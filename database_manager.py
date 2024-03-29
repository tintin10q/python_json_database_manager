import copy
import glob
import json
import time
import shutil
import os
from multiprocessing import Lock

from collections import UserDict


__author__ = 'Quinten Cabo'
__license__ = 'GNUV2'


class Database(UserDict):
    """
    This class is used to write and read stuff with a database made out of local json files

    The files are being read from disk and turned into dicts.
    This class really shines with the context manager where you just ask for the name of a document and you
    can edit it as a dict.
    The dict is automatically written to disk when the context manager is closed.

    _save functions can be run on the class outside a context manager as they acquire the lock for the file.
    functions without save are only meant to be run inside a with statement that will lock the file for them.

    When reading you can call the static methods.

    Database.read(name)

    It is not recommended to use the write methods use the context manager instead.
    When using the context manager make an instance of the class.

    with Database("document_name") as document:
        document_name["new_data"] = new_data

    Document will be a dict so you can use document as if it is a dict!

    If anything goes wrong with the context manager makes a rollback to the state before any edits is made!

    You can call create_backup(documents: list[str] = "all_of_them") to create a backup of documents
    These will be put in a backup folder in a sub folder with a date. You can either give a list of document names
    or just the string "all_of_them" which is the default for all documents to be backed up.
    """

    # You can set the backup dir name here
    backup_directory_name = "json_db_backups"
    my_path = os.path.dirname(os.path.realpath(__file__))  # Get the place of this file with realpath
    backup_folder_path = os.path.join(my_path, backup_directory_name)
    
    # generate locks
    locks = {os.path.basename(file[:-5]): Lock() for file in glob.iglob(os.path.join(my_path, "*.json"))}

    @staticmethod
    def info():
        return {
            "backup_directory_name": Database.backup_directory_name,
            "my_path": Database.my_path,
            "backup_folder_path": Database.backup_folder_path,
            "locks": Database.locks
        }

    def __init__(self, filename: str):
        self.__name = filename
        self.__in_with = False  # This is a boolean which is true when the Object __enter__ has been called and __exit__ has not yet been called. Used for __contains__
        super().__init__()

    @property
    def lock(self):
        """Returns appropriate lock for file with self.name."""
        assert self.name in Database.locks, "You are trying to acces a database that does not exist."
        return Database.locks[self.name]

    @staticmethod
    def get_lock(name: str):
        """Returns lock based on input name."""
        return Database.locks[name]

    @property
    def name(self):
        """ Name of the current selected json file """
        return self.__name

    @name.setter
    def name(self, name: str):
        assert name in Database.locks, "You are trying to switch to a name that does not exist in the database."
        self.__name = name

    @staticmethod
    def read(name: str):
        """Will read <name>.json with a lock. Do not run in other lock that will cause deadlock"""
        with Database.get_lock(name):
            database = Database.__read(name)
        return database

    @staticmethod
    def __read(name: str):
        """ Will read <name>.json without a lock. Maybe rename this to _read_unsafe? """
        database_path = os.path.join(os.path.dirname(__file__), name + ".json")
        with open(database_path, "r+") as database_file:
            database = json.load(database_file)
        return database

    def reads(self):
        """ Will read <self.name>.json without a lock. """
        return Database.__read(self.name)

    @staticmethod
    def write(name: str, data: dict):
        """ Will write data to the <name>.json with a lock. Do not run in other lock that will cause a deadlock! 
            ALso do not run this in general use the context manager.
        """
        with Database.get_lock(name):
            return Database.__write(name, data)

    @staticmethod
    def __write(name: str, data: dict):
        """ Will write data to <name>.json without a lock. Maybe rename this to _write_unsafe? """
        database_path = os.path.join(os.path.dirname(__file__), name + ".json")
        with open(database_path, "w+") as file:
            json.dump(data, file, indent=4, sort_keys=True)

    def writes(self, data: dict = None):
        """ Will write data to <self.name>.json without a lock.
            If data is None it will write self.data
        """
        if data is None:
            self.__write(self.name, self.data)
        else:
            self.__write(self.name, data)

    @staticmethod
    def create(name: str, data: dict = None, replace: bool = False):
        """ Will create a new file named <name>.json with data inside and will add file to lock. """
        if data is None:
            data = dict()
        if name not in Database.locks:
            Database.locks[name] = Lock()
            database_path = os.path.join(os.path.dirname(__file__), name + ".json")
            open(database_path, "w+").close()
            Database.write(name, data)
            return data
        elif name in Database.locks and replace:  # File already there
            database_path = os.path.join(os.path.dirname(__file__), name + ".json")
            open(database_path, "w+").close()
            Database.write(name, data)
            return data

    @staticmethod
    def add(name: str, key: str, data: dict):
        """ Will try to add the data under the identifier to the specified file. If the data is already in this file
        it will override this data. This is a (probably faster) shorthand for combining get and set. """
        with Database.get_lock(name):
            database = Database.__read(name)
            database[key] = data
            Database.__write(name, database)

    def adds(self, key, data: dict):
        """ Will try to add the data under the identifier to the specified file. If the data is already in this file
        it will override this data. This is a shorthand for combining get and set. """
        with self.lock:
            database = self.reads()
            database[key] = data
            self.writes(database)

    @staticmethod
    def append(name, data):
        """ Will append database to a list named <name> in a file named <name>.json. """
        with Database.get_lock(name):
            database = Database.__read(name)
            database[name].append(data)
            Database.__write(name, database)

    def appends(self, data):
        """ Will append database to a list named <self.name> in a file named <self.name>.json. """
        with self.lock:
            database = self.reads()
            database[self.name].append(data)
            self.writes(database)

    @staticmethod
    def reset_all(default_data: dict):
        """ Will reset all databases. The reset state should be registered manually for special cases. """
        for name in Database.locks.keys():
            Database.write(name, default_data)

    @staticmethod
    def translate(name, key):
        """ Will translate a name to the corresponding ID """
        return Database.read(name)[key]

    def translates(self, key):
        """ Will translate a name to the corresponding ID """
        return self.reads()[key]

    def __enter__(self):
        self.__in_with = True
        self.clear()
        self.lock.acquire()
        self.data = self.reads()
        self.backup_data = copy.deepcopy(self.data)  # Make a deep copy to preserve the backup and also lists inside the backup
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:  # There was an error in context attempt rollback
                try:  # Try to write new data
                    self.writes()
                except TypeError as e:  # This can happen if data is not json serializable, Attempt rollback and then raise the error to notify
                    self.__write(self.name, self.backup_data)
                    raise e
        finally:
            self.__in_with = False
            self.lock.release()

    @staticmethod
    def create_backup(document_names: list[str] = "all_of_them"):
        """
        Makes backups in a backup folder with the date
        :param document_names:
        """

        if document_names == "all_of_them":
            document_names = Database.locks.keys()

        if len(document_names) <= 0:
            return

        locks = Database.locks
        timestring = time.strftime("%Y%m%d-%H%M%S")

        if not os.path.exists(Database.backup_folder_path):
            os.mkdir(Database.backup_folder_path)

        backup_path = os.path.join(Database.backup_folder_path, timestring)

        os.mkdir(backup_path)

        for document_name in document_names:
            filename = document_name
            if not filename.endswith(".json"):
                filename += ".json"
            src = os.path.join(Database.my_path, filename)
            dst = os.path.join(backup_path, filename)
            with locks[document_name]:
                shutil.copy2(src, dst)

    def __contains__(self, key):
        """ This can cause a deadlock if you are not carefull.
            The contains can now detect if it is in a with statement and will not cause a deadlock when it is.
        """

        if self.__in_with:
            return key in self.data  # Check if the key is in the data that __enter__ read.
        else:
            with self.lock:  # Lock read
                return key in self.reads()

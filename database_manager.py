import glob
import json
import os
import threading


class Database(dict):
    """
    This class is used to write and read stuff with the database
    _save functions can be run on the class as they acquire the lock for the file.
    functions without save are only meant to be run inside a with statement that will lock the file for them.

    """

    # generate locks
    my_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(my_path)
    locks = {file[:-5]: threading.Lock() for file in glob.glob("*.json")}

    def __init__(self, filename):
        self.__name = filename
        super().__init__()

    @property
    def lock(self):
        """Returns appropriate lock for file with self.name."""
        assert self.name in Database.locks, "You are trying to acces a database that does not exist."
        return Database.locks[self.name]

    @staticmethod
    def get_lock(name):
        """Returns lock based on input name."""
        return Database.locks[name]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        assert name in Database.locks, "You are trying to switch to a name that does not exist in the database."
        self.__name = name

    @staticmethod
    def read(name):
        """Will read <name>.json with a lock. Do not run in other lock that will cause deadlock"""
        with Database.get_lock(name):
            database = Database.__read(name)
        return database

    @staticmethod
    def __read(name):
        """Will read <name>.json without a lock. Maybe rename this to _read_unsafe?"""
        database_path = os.path.join(os.path.dirname(__file__), name + ".json")
        with open(database_path, "r+") as database_file:
            database = json.load(database_file)
        return database

    def _readself(self):
        """Will read <self.name>.json without a lock."""
        return Database.__read(self.name)

    @staticmethod
    def write(name, data):
        """Will write data to the <name>.json with a lock. Do not run in other lock that will cause deadlock."""
        with Database.get_lock(name):
            return Database.__write(name, data)

    @staticmethod
    def __write(name, data):
        """Will write data to <name>.json without a lock. Maybe rename this to _write_unsafe?"""
        database_path = os.path.join(os.path.dirname(__file__), name + ".json")
        with open(database_path, "w+") as file:
            json.dump(data, file, indent=4, sort_keys=True)

    def _writeself(self):
        """Will write self:dict to <self.name>.json without a lock."""
        Database.__write(self.name, self)

    @staticmethod
    def create(name, data={}):
        """Will create a new file named <name>.json with data inside and will add file to lock."""
        assert name not in Database.locks, "You tried to create a database that already exists."
        database_path = os.path.join(os.path.dirname(__file__), name + ".json")
        open(database_path, "w+").close()
        Database.locks[name] = threading.Lock()
        Database.write(name, data)
        return data

    @staticmethod
    def add(name, data, key):
        """ Will try to add the data under the identifier to the specified file. If the data is already in this file
        it will override this data. This is a shorthand for combining get and set."""
        with Database.get_lock(name):
            database = Database.__read(name)
            database[key] = data
            Database.__write(name, database)

    @staticmethod
    def append(name, data):
        """ Will append database to a list named <name> in a file named <name>.json."""
        with Database.get_lock(name):
            database = Database.__read(name)
            database[name].append(data)
            Database.__write(name, database)

    @staticmethod
    def reset_all(default_data={}):
        """Will reset all databases. The reset state should be registered manually for special cases."""
        for name, lock in Database.locks.items():
            with lock:
                Database.write(name, default_data)
        return

    @staticmethod
    def translate(name, key):
        """ Will translate a name to the corresponding ID """
        if name in (translations := Database.__read(name)):
            return translations[key]
        else:
            return False

    def __enter__(self):
        self.clear()
        self.lock.acquire()
        self.backup_data = self._readself()
        self.update(self.backup_data)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:  # Attempt rollback
                self.__write(self.name, self.backup_data)
            else:
                self._writeself()
        finally:
            Database.locks[self.name].release()
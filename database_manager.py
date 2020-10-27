import copy
import glob
import json
import os
import threading


class Database(dict):
    """
    This class is used to write and read stuff with the database
    _save functions can be run on the class as they acquire the lock for the file.
    functions without save are only meant to be run inside a with statement that will lock the file for them.
    
    When reading you can call the static methods. 
    
    Database.read(name)
    
    It is not recomended to use the write methods use the context manager instead.
    When using the context manager make an instance of the class.
    
    with Database(name) as name:
        bla bla bla
        
    name will be a dict so you can use name as if it is a dict!
    If anything goes wrong with the context manager a rollback will be made. 
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
        """Will write data to the <name>.json with a lock. Do not run in other lock that will cause deadlock. ALso do not run this in general use the context manager"""
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
    def create(name, data, replace=False):
        """Will create a new file named <name>.json with data inside and will add file to lock."""
        if name not in Database.locks:
            Database.locks[name] = threading.Lock()
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
    def reset_all(default_data):
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
        self.data = self._readself()
        self.backup_data = copy.deepcopy(self.data)  # Make a deep copy to preserve the backup and also lists inside the backup
        self.update(self.data)  # Set dict data to self.data
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:  # There was an error in context attempt rollback and re-raise
                self.__write(self.name, self.backup_data)
                raise exc_type
            else:
                try:  # Try to write new data
                    self._writeself()
                except TypeError as e:  # This can happen if data is not json serializable, Attempt rollback
                    self.__write(self.name, self.backup_data)
                    raise e
        finally:
            Database.locks[self.name].release()

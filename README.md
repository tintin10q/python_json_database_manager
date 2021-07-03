# python-json-database-manager
The database manager used in many of my projects

A thread safe json database context manager. The class creates seperate locks for each .json file in the same directory as the .py file. This way if one file is edited other files do not have to wait.

## This class can be used with the `with` statement.

```
db = Database

with db('test') as users:
    users["quinten"] = {"status": "cool"}
    users["foo"] = "bar"
```

The context manager will automatically fetch the data that is in the .json file and make sure this code runs in a lock specefic to the file in the __enter__ and will in the __exit__ write the modified dictionary back to the file. If any unhandeld erros happen in the with no data is written back to the file. 

You can initiate the class with a target name. The class checks if this file exists. If it does then the `with` statement will write the dictionary to that file. 

You can also change the target name by modifing self.name. There is an automatic check that will assert if this new name exists. 

## Static methods
There are also a couple static methods for when you do not want to run a database command in a `with`. All of these static methods will all acquire the lock for the file automatically. 

- `create_backup(filenames: list[str])` -> Makes a backup of all .json files in a the backup folder. The default backup location is `json_db_backups`. Give "all_of_them" as input to backup all files. This is the default.
- `read(name)` -> Will return the **data** in **name**.json
- `write(name,data)` -> Will write **data** to **name**.json
- `add(name, data key)` -> Will add/replace **data** under **key** in **name**.json. A shorthand for read + write.
- `append(name, data)` -> Will append **data** to a list named **name** in **name**.json 
- `reset_all(default_data)` -> Will write **default_data** to all databases. You can implement your own exeptions here.
- `translate(name, key)` -> Will return the value for **key** in **name**.json. Usefull for 1 layer dicts.
- `create(name, data)` -> Will create a new **name**.json in the db dir', write **data** to it and will add a new lock. Do not create json files without this method as the database does only index json files on startup. 

There are also versions of these methods that end in 's. These don't take a name but instead look at self.name to know which file it should interact with. 

'db dir = Directory with the database_manager.py

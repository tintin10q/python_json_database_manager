import time
import unittest
import json
import os
from database_manager import Database
from threading import Thread

test_name = "___testing"
test_filename = test_name + ".json"
test_data = {
    "1": 1,
    "test": "test",
    "list": ["1", 2, {"3": 3}],
    "dict": {"test": "data"}
}


class TestDbStatic(unittest.TestCase):

    def setUp(self) -> None:
        """ Create a ___testing.json
            In setup we are assuming that .create works so that one is in a separate testcase
        """

        Database.create(test_name, test_data, replace=True)

    def tearDown(self) -> None:
        """ Remove the test json file """
        os.remove(test_name + ".json")

    def test_lock_property(self):
        db = Database(test_name)
        self.assertEqual(db.lock, db.locks[test_name])

    def test_get_lock(self):
        self.assertEqual(Database.get_lock(test_name), Database.locks[test_name])

    def test_name_property(self):
        db = Database(test_name)
        self.assertEqual(db.name, test_name)

    def test_read(self):
        self.assertEqual(Database.read(test_name), test_data)

    def test_write(self):
        data = {"woah": ['1', '2', '3'], "some": "test", "data": 1}
        Database.write(test_name, data)
        self.assertEqual(Database.read(test_name), data)

    def test_add(self):
        Database.add(test_name, "some_key", "some_data")
        data = Database.read(test_name)
        self.assertIn("some_key", data)
        self.assertEqual(data["some_key"], "some_data")

        Database.add(test_name, "some_key", {"some_data": 1})
        data = Database.read(test_name)
        self.assertIn("some_key", data)
        self.assertEqual(data["some_key"], {"some_data": 1})

    def test_append(self):
        Database.write(test_name, {test_name: []})
        Database.append(test_name, "hi")
        data = Database.read(test_name)
        self.assertIn(test_name, data)
        self.assertIn("hi", data[test_name])
        Database.append(test_name, "hi2")
        data = Database.read(test_name)
        self.assertIn(test_name, data)
        self.assertIn("hi", data[test_name])
        self.assertIn("hi2", data[test_name])
        Database.append(test_name, "hi")

    def test_translate(self):
        self.assertEqual(Database.translate(test_name, "test"), "test")
        self.assertEqual(Database.translate(test_name, "1"), 1)

    def test_info(self):
        self.assertTrue(type(Database.info == dict), "Database.info did not return a dict")
        self.assertIn("backup_directory_name", Database.info(), "Database.info does not have backup_directory_name")
        self.assertIn("my_path", Database.info(), "Database.info does not have my_path")
        self.assertIn("backup_folder_path", Database.info(), "Database.info does not have backup_folder_path")
        self.assertIn("locks", Database.info(), "Database.info does not have locks")


class TestDatabaseInstance(unittest.TestCase):
    def setUp(self) -> None:
        """ Create a ___testing.json
            In setup we are assuming that .create works so that one is in a seperate testcase
        """

        Database.create(test_name, test_data, replace=True)

    def tearDown(self) -> None:
        """ Remove the test json file """
        os.remove(test_name + ".json")

    def test_translates(self):
        db = Database(test_name)
        self.assertEqual(db.translates("test"), "test")
        self.assertEqual(db.translates("1"), 1)

    def test_appends(self):
        db = Database(test_name)
        db.writes({test_name: []})
        db.append(test_name, "hi")
        data = db.reads()
        self.assertIn(test_name, data)
        self.assertIn("hi", data[test_name])
        db.appends("hi2")
        data = db.reads()
        self.assertIn(test_name, data)
        self.assertIn("hi", data[test_name])
        self.assertIn("hi2", data[test_name])
        Database.append(test_name, "hi")

    def test_adds(self):
        db = Database(test_name)
        db.adds("some_key", "some_data")
        data = db.reads()
        self.assertIn("some_key", data)
        self.assertEqual(data["some_key"], "some_data")

        db.adds("some_key", {"some_data": 1})
        data = db.reads()
        self.assertIn("some_key", data)
        self.assertEqual(data["some_key"], {"some_data": 1})

    def test_writes(self):
        db = Database(test_name)
        db.data = {"woah": ['1', '2', '3'], "some": "test", "data": 1}
        db.writes()
        self.assertEqual(db.reads(), db.data)
        db.writes({"woah": ['1', '2', '3'], "some": "test", "data": 1})
        self.assertEqual(db.reads(), {"woah": ['1', '2', '3'], "some": "test", "data": 1})

    def test_reads(self):
        db = Database(test_name)
        self.assertEqual(db.reads(), test_data)

    def test__contains__(self):
        db = Database(test_name)
        self.assertTrue("test" in db)
        self.assertTrue("1" in db)
        self.assertFalse("2" in db)

    def test__contains__in_with(self):
        with Database(test_name) as db:
            self.assertTrue("test" in db)
            self.assertTrue("1" in db)
            self.assertFalse("2" in db)

    def test__in_with(self):
        """ Test if __in_with property is set correctly. This property is needed for __contains__ to not deadlock in a with """
        db = Database(test_name)
        self.assertFalse(db.__dict__['_Database__in_with'])
        with db as dbwith:
            self.assertTrue(dbwith.__dict__['_Database__in_with'])
            self.assertTrue(db.__dict__['_Database__in_with'])
        self.assertFalse(db.__dict__['_Database__in_with'])
        self.assertFalse(dbwith.__dict__['_Database__in_with'])

    def test_context_manager(self):
        with Database(test_name) as db:
            db["aapje"] = "aapje"
            db["aapje1"] = ["aapje"]
        data = Database.read(test_name)
        self.assertEqual(data["aapje"], "aapje")
        self.assertEqual(data["aapje1"], ["aapje"])

    def test_context_manager_with_error(self):
        with self.assertRaises(KeyError):
            with Database(test_name) as db:
                db["aapje"] = "aapje"
                raise KeyError
        data = Database.read(test_name)
        self.assertNotIn("aapje", data)

    def test_context_manager_with_malformed(self):
        with self.assertRaises(TypeError):
            with Database(test_name) as db:
                db["aaa"] = "aaa"
                db["aapje"] = Exception  # It can't write this so no data is written
        data = Database.read(test_name)
        self.assertNotIn("aapje", data)
        self.assertNotIn("aaa", data)

    def test_thread_save(self):
        """ This should take 1 second showing that the threads waited on each other"""
        db = Database(test_name)

        wait_time = 0.5

        def thread_write(databse_object: Database, _id: int, data: str):
            with databse_object as dbs:
                dbs["thread"] = _id
                time.sleep(wait_time)
                dbs["thread_data"] = data

        s = time.time()
        t = Thread(target=thread_write, args=(db, 1, "lala1"))
        t2 = Thread(target=thread_write, args=(db, 2, "lala2"))
        t.start()
        t2.start()
        t.join()
        t2.join()
        s1 = time.time()
        data = Database.read(test_name)
        self.assertEqual(data["thread"], 2)
        self.assertEqual(data["thread_data"], "lala2")
        self.assertAlmostEqual(s1 - s, wait_time * 2, 1)  # times 2 because there are 2 threads


class TestCreateBackups(unittest.TestCase):
    def setUp(self) -> None:
        """ Create a ___testing.json
        In setup we are assuming that .create works so that one is in a seperate testcase"""
        Database.create(test_name, test_data, replace=True)
        os.mkdir(Database.backup_folder_path)
        self.backups_already_there = set(os.listdir(Database.backup_folder_path))

    def tearDown(self) -> None:
        """ Remove the test json file """
        os.remove(os.path.join(self.new_file_full_path, test_filename))
        os.removedirs(self.new_file_full_path)

    def test_create_backup(self):
        Database.create_backup([test_name])
        self.assertTrue(os.path.exists(Database.backup_folder_path))  # is backup folder there
        files_in_backup_dir = set(os.listdir(Database.backup_folder_path))
        self.assertTrue(len(files_in_backup_dir) == len(self.backups_already_there) + 1)  # is another folder added
        self.new_file_list = list(files_in_backup_dir - self.backups_already_there)
        self.new_file_full_path = os.path.join(Database.backup_folder_path, self.new_file_list[0])
        self.assertEqual(len(self.new_file_list), 1)
        self.assertEqual(len(os.listdir(self.new_file_full_path)), 1)


class TestDBCreate(unittest.TestCase):

    def test_create(self):
        Database.create(test_name, test_data)
        # Is the file there
        self.assertTrue(os.path.exists(test_filename))
        # Does the file have the data
        with open(test_filename) as f:
            self.assertEqual(json.load(f), test_data)
            # is the lock added
            self.assertIn(test_name, Database.locks)

        with open(test_filename) as f:
            # does replace=True/False work
            Database.create(test_name, {"hi": "there!"})  # Should not be created!
            self.assertEqual(json.load(f), test_data)
        with open(test_filename) as f:
            Database.create(test_name, {"hi": "there"}, replace=True)
            self.assertEqual(json.load(f), {"hi": "there"})

        with open(test_filename) as f:
            Database.create(test_name, {"hi": "there2"})
            self.assertEqual(json.load(f), {"hi": "there"})

    def tearDown(self) -> None:
        """ Remove the test json file """
        os.remove(test_filename)


if __name__ == '__main__':
    unittest.main()

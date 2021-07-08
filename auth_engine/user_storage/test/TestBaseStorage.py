
import unittest

from user_storage import BaseStorage

class TestBaseStorage(unittest.TestCase):
	def test_has_crud_attributes(self):
		storage = BaseStorage()
		self.assertTrue(hasattr(storage, "read_user"))
		self.assertTrue(hasattr(storage, "update_user"))
		self.assertTrue(hasattr(storage, "merge_user"))
		self.assertTrue(hasattr(storage, "delete_user"))
		self.assertTrue(hasattr(storage, "__contains__"))
		self.assertTrue(hasattr(storage, "already_exits"))
	
	def test_static_attributes(self):
		self.assertTrue(hasattr(BaseStorage, "already_exits"))
	
	def test_raises_not_implemented(self):
		storage = BaseStorage()
		user_id = "blabla"
		with self.assertRaises(NotImplementedError):
			storage.create_user(user_id)
			storage.read_user(user_id)
			storage.update_user(user_id, user_id)
			storage.merge_user(user_id, user_id)
			storage.delete_user(user_id)

	
if __name__ == '__main__':
	unittest.main()

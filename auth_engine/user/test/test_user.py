from user import User
from user_storage import MemoryUserStorage

import unittest


class TestUser(unittest.TestCase):
	
	def test_create_with_only_id(self):
		""" If a user is created with only an id the data of the user should be the standard data """
		user_id = "some_user_id"
		standard_data = {User._user_id_key: user_id, User._verified_key: False, User._verified_data_key: {}}
		user = User(user_id)
		self.assertEqual(user, standard_data)
	
	def test_create_with_data(self):
		"""Test the behavior if you create a user with a user id and data given but no storage
			If the standard keys are not in the data they are added in this case so test for that
		"""
		some_user = User("some_id", data={})
		
		# Are the standard keys added if they are not there
		self.assertIn(User._user_id_key, some_user)
		self.assertIn(User._verified_key, some_user)
		self.assertIn(User._verified_data_key, some_user)
		self.assertNotIn(User._email_key, some_user)  # Email should not be added
		self.assertFalse(some_user[User._verified_key])
		self.assertEqual(some_user[User._verified_data_key], {})
		
		# id is always added
		some_user = User("some_id", data={User._user_id_key: "some_other_id"})
		self.assertEqual(some_user.data[User._user_id_key], "some_id")
		self.assertNotEqual(some_user.data[User._user_id_key], "some_other_id")
		
		# Are the other standard keys not added if they are there
		some_user = User("some_id", data={User._verified_data_key: ["I", "AM", "A LIST", "NOW"], User._verified_key: True})
		self.assertEqual(some_user[User._verified_data_key], ["I", "AM", "A LIST", "NOW"])
		self.assertTrue(some_user[User._verified_key])
		self.assertIn(User._user_id_key, some_user)
		self.assertEqual(some_user[User._user_id_key], "some_id")
	
	def test_is_verified_property(self):
		""" Test if the is_verified property works """
		
		# Default is not verified
		some_user = User("some_id", data={})
		self.assertFalse(some_user.is_verified)
		
		# Test if user is not verified if we say the user is not verified
		user_not_verified = User("some_id", data={User._user_id_key: "some_id", User._verified_key: False})
		self.assertFalse(user_not_verified.is_verified)
		
		# Test if the user is verified if we say the user is verified
		user_verified = User("some_id", data={User._user_id_key: "some_id", User._verified_key: True})
		self.assertTrue(user_verified.is_verified)
	
	def test_is_known_property(self):
		"""
			Tests the is_known property. This only tests that it returns False if there is not storage
			Returning True needs a working storage and so its in the other test case
		"""
		unknown_user = User("some_user")
		self.assertFalse(unknown_user.is_known)
	
	def test_verified_data_property(self):
		#  Is verified data there if you create with only an id
		some_user = User("some_user_id")
		self.assertEqual(some_user.verified_data, {})
		
		#  Is the property mapped to the right key
		some_user[User._verified_data_key] = {"token1": "some_token1"}
		self.assertIn("token1", some_user.verified_data)
		self.assertEqual(some_user.verified_data["token1"], "some_token1")
		
		#  Does the setter work
		some_user.verified_data = {"token2": "some_token2"}
		self.assertIn("token2", some_user.verified_data)
		self.assertIn("token2", some_user.data[User._verified_data_key])
		self.assertEqual(some_user.verified_data["token2"], "some_token2")
		self.assertEqual(some_user.data[User._verified_data_key]["token2"], "some_token2")
		
		#  Can you index the property
		some_user = User("some_user_id")
		some_user.verified_data["token"] = "some_token"
		self.assertIn("token", some_user.verified_data)
		self.assertEqual(some_user.verified_data["token"], "some_token")
		
		#  Does it read from User._verified_data_key
		some_user.pop(User._verified_data_key)
		with self.assertRaises(KeyError):
			v = some_user.verified_data
	
	def test_has_email_property(self):
		""" Tests if the has_email property works """
		some_user = User("some_id")
		self.assertFalse(some_user.has_email)
		
		# Reads from the right key
		some_user = User("some_id", data={User._email_key: "some_email@email.com"})
		self.assertTrue(some_user.has_email)
	
	def test_email_property(self):
		""" Tests if the email property works well """
		#  Raises KeyError if it is not there
		some_user = User("some_id")
		with self.assertRaises(KeyError):
			email = some_user.email
		
		#  Does email take from the right key
		some_user = User("some_id", data={User._email_key: "my_email@email.com"})
		self.assertEqual(some_user.email, "my_email@email.com")
		
		#  Does the setter work
		some_user.email = "new_email@email.com"
		self.assertEqual(some_user.email, "new_email@email.com")
		self.assertEqual(some_user[User._email_key], "new_email@email.com")
		self.assertNotEqual(some_user.email, "my_email@email.com")
		self.assertNotEqual(some_user[User._email_key], "my_email@email.com")
	
	def test_email_and_has_email(self):
		user = User("some_id")
		self.assertFalse(user.has_email)
		user.email = "my_email@mail.com"
		self.assertTrue(user.has_email)
		
	def test_user_id_property(self):
		some_user = User("some_id")
		self.assertEqual(some_user.user_id, "some_id")
		
		# trying to set user_id raises attribute error
		with self.assertRaises(AttributeError):
			some_user.user_id = "some_new_id"
		
		# check if it is reading from the right key
		some_user[User._user_id_key] = "new_id"
		self.assertEqual(some_user.user_id, "new_id")
	
	def test_linked_to_storage_property(self):
		""" Test if linked to storage is working.
			Linked to storage just checks if storage is not None and  if storage is an instance of BaseStore
			We need a working storage to create a user with a storage so this test is also in the other testcase.
		"""
		# Just check if it is False if you don't even give a storage
		some_user = User("some_id")
		self.assertFalse(some_user.linked_to_storage)
		
		with self.assertRaises(AttributeError):
			some_user.linked_to_storage = False
		
		
	def test_get_id(self):
		""" Tests the get_id User function """
		self.assertEqual(User.get_id("1234"), "1234")
		self.assertEqual(User.get_id(User("1234")), "1234")
		self.assertEqual(User.get_id({User._user_id_key:"1234"}), "1234")
		with self.assertRaises(KeyError):
			User.get_id({})
		with self.assertRaises(NotImplementedError):
			User.get_id(())
			User.get_id([])
			User.get_id(12345)
			User.get_id(BaseException)
			User.get_id(User)
			User.get_id(set())
	
	def test_has_valid_email(self):
		some_user = User("some_id")
		some_user.email = "notarealemail"
		self.assertFalse(some_user.has_valid_email)
		some_user.email = "realemail@email.com"
		self.assertTrue(some_user.has_valid_email)

class TestUserAndStorageInteraction(unittest.TestCase):
	"""
	This test case has all the interactions with the storage.
	So this has all the test that need a working storage.
	"""
	
	storage_class = MemoryUserStorage
	
	def test_create_with_storage(self):
		"""
			If a user is created with a storage then the data should come from the storage
		"""
	
	def test_linked_to_storage_property(self):
		pass
	
	def test_sync_from_storage(self):
		pass
	
	def test_sync_to_storage(self):
		pass

	def test_linked_to_storage_property(self):
		pass

	def test_is_known(self):
		pass
	
if __name__ == '__main__':
	unittest.main()

from __future__ import annotations

from collections import UserDict

from user import User


class BaseStorage():
	"""
	The users are stored in a storage. This is the base storage object other storages should inherit from.
	For each of these functions you can either give just the users string id or pass a User object.
	If a user object is passed then that data is used.
	If a user_id is passed the user with that id is read from the storage first.
	"""
	
	def create_user(self, user: User = None):
		"""" Creates a user in the database
		If the user given is None a new user with a new id is made. This user will not be verified.

		If the user already exists then UserAlreadyExists is raised
		"""
		raise NotImplementedError
	
	def read_user(self, user: User) -> User:
		""" Reads the data from the user """
		raise NotImplementedError
	
	def update_user(self, user_to_update: User, user_to_update_with: User, save_id: bool = True):
		"""
			Updates the user record
			The user given will replace the user in the database
			:param user_to_update: The user to update can be string id or user object
			:param user_to_update_with: The user to update with. Has to be dictlike
			:param save_id: Whether or not to make sure the id of the user_to_update does not change
		"""
		raise NotImplementedError
	
	def merge_user(self, user_to_update: User, user_to_merge_with: User, save_id: bool = True):
		"""
		Merges the data of the user given and the user in the database with the given id.
		The standard keys of the user id, email  and verified status input SHOULD NOT BE MERGED!
		:param user1: user2 will be merged into user1
		:param user2: user that will be merged into user1
		
		:return: User
		"""
		raise NotImplementedError
	
	def delete_user(self, user: User) -> User:
		"""" Deletes a user from the database """
		raise NotImplementedError
	
	def __contains__(self, item):
		""" Can take another user object or a user id string """
		user_id = User.get_id(item)
		try:
			self.read_user(user_id)
			return True
		except KeyError:
			return False
	
	@staticmethod
	def already_exits(user) -> bool:
		"""
		Returns true if the user is already found in the database
		:returns bool
		"""
		raise NotImplementedError
	
	def create_user_object(self, user_data: dict) -> User:
		"""
			Creates a user object from a dict,
			The data is passed as data so we don't read again from the database on user creation.
			So use this method if you don't want to read from the storage again on user creation.

			:param user_data: the dict from which the user object is made
			:return User object
			:returns User
		"""
		user_id = User.get_id(user_data)
		return User(user_id, storage=self, data=user_data)

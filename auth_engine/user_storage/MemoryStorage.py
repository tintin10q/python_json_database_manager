from __future__ import annotations

from user_storage.BaseStorage import BaseStorage
from user_storage.exceptions import UserAlreadyExists
from contextlib import contextmanager
from user_storage.exceptions import IdMixup
import uuid
from user import User


class MemoryUserStorage(BaseStorage):
	users = {}
	aliases = {}
	
	def __init__(self):
		self.users = MemoryUserStorage.users
		self.aliases = MemoryUserStorage.aliases
	
	def create_user(self, user: User = None) -> User:
		"""
		Adds a user to the database. Will raise UserAlreadyExists if the user is already in the database
		
		if user is None a default empty user is made with a unique id
		if user is a string a default empty user is made with the string as id
		if user is a user object the data is used from the user object to create the user in the database
		:param user:
		"""
		
		if user is None:
			new_id = str(uuid.uuid4())
			new_user_data = {
				User._user_id_key: new_id,
				User._verified_key: False,
				User._verified_data_key: {},
				User._email_key: None
			}
			self.users[new_id] = new_user_data
			return self.create_user_object(new_user_data)
		
		elif isinstance(user, str):
			if self.already_exits(user):
				raise UserAlreadyExists(user)
			
			user_id = User.get_id(user)
			
			# just add the id and required tags all being None except id defaults
			new_user_data= {
				User._user_id_key: user_id,
				User._verified_key: False,
				User._verified_data_key: {},
			}
			self.users[user_id] = new_user_data
			return self.create_user_object(new_user_data)
		
		elif isinstance(user, User):

			if self.already_exits(user):
				raise UserAlreadyExists(user)
			
			new_user_data = {}
			new_user_data |= user
			new_user_data |= {
				User._user_id_key: user.user_id,
				User._verified_data_key: user.verified_data,
				User._verified_key: user.is_verified
			}   # Enforce defaults
			
			self.users[user.user_id] = new_user_data
			return self.create_user_object(new_user_data)
	
	def read_user(self, user_id: str, skip_aliases: bool = False) -> User:
		""" Reads and returns a user, can be string or user object """
		
		try:
			user_data = self.users[user_id]
		except KeyError as key_error:
			if skip_aliases:
				raise key_error
			new_user_id = self.aliases[user_id]
			user_data = self.users[new_user_id]
		
		return self.create_user_object(user_data)
	
	
	def update_user_key(old_key: str, new_key: str, check_for_alias: bool = False):
		"""
		Changes a the key a user is saved under
		The id in the user is also changed to the new_key
		:param user: The user object which key has to be changed. Can be string or user object
		:param new_key: The new key you want the user to be under
		:param check_for_alias: do you want to go trough the alias file and rename the old id to the new id
		
		:raise UserAlreadyExists
		"""
		new_key_id = User.get_id(new_key)
		
		if MemoryUserStorage.already_exits(new_key):
			raise UserAlreadyExists(new_key)
		
		old_user_id = User.get_id(new_key)
		old_user_data = dict(MemoryUserStorage.users[old_user_id]) # make a copy and get the data
		
		del MemoryUserStorage.users[old_user_id]
		
		MemoryUserStorage.users[new_key] = old_user_data
		MemoryUserStorage.users[new_key][User._user_id_key] = new_key
		
		if check_for_alias:
			MemoryUserStorage.replace_alias(old_user_id, new_key)
	
	@staticmethod
	def replace_alias(old_alias: str, new_alias: str):
		"""
		Replaces an old alias with a new alias.
		The key will stay the same but the value the alias points to is changed.
		:param old_alias: The old alias value
		:param new_alias: The new alias value
		:return:
		"""
		if old_alias in MemoryUserStorage.aliases.values():
			for key, value in MemoryUserStorage.aliases.items():
				if value == old_alias:
					MemoryUserStorage.aliases[key] = new_alias
	
	def update_user(self, user_to_update: User, user_to_update_with: User, save_id: bool = True) -> User:
		"""
			Updates the user record
			The user given will replace the user in the database
		"""
		user_id = User.get_id(user_to_update)
		if save_id:
			user_to_update_with[User._user_id_key] = user_id
		self.users[user_id] = dict(user_to_update)
		return User(user_id, storage=self)
	
	def merge_user(self, user_to_update: User, user_to_merge_with: User, save_id=True) -> User:
		""" Merges instead of replaces a user
		    Id is changed back to ensure it stays the same """
		user_id = User.get_id(user_to_update)
		if save_id:
			user_to_merge_with[User._user_id_key] = user_id
		self.users[user_id] |= user_to_merge_with
		return User(user_id, storage=self)
	
	def delete_user(self, user: User) -> User:
		"""" Deletes a user from the database """
		user_id = User.get_id(user)
		return self.users.pop(user_id)
	
	@staticmethod
	def already_exits(user) -> bool:
		""" Returns true if the user is already found in the database :returns bool """
		user_id = User.get_id(user)
		if user_id in MemoryUserStorage.users:
			return True
		else:
			try:
				translated_user_id = MemoryUserStorage.aliases[user_id]
				if translated_user_id in MemoryUserStorage.users:
					return True
			except KeyError:
				return False
	
	@staticmethod
	def create_alias(real_id: User, alias: str, force=True):
		"""
		Creates a way to have multiple ids for a user. If the first id is not found the read user will check the
		aliases
		"""
		real_id = User.get_id(real_id)
		if MemoryUserStorage.already_exits(real_id):
			raise UserAlreadyExists(real_id, message=f"Can't use an id that already exists as an alias, id: {real_id}")
		MemoryUserStorage.aliases[alias] = real_id
	
	@staticmethod
	def delete_alias(alias: str):
		"""
		Removes an alias from the alias json
		:param alternate_id:
		"""
		del MemoryUserStorage.aliases[alias]
	
	@contextmanager
	def yield_user_context(self, user: User) -> User:
		"""
		The context manages will merge the user again after the with.
		:param user:
		"""
		user_id = User.get_id(user)
		user_object = self.read_user(user_id)
		yield user_object
		
		self.merge_user(user_id, user_object)

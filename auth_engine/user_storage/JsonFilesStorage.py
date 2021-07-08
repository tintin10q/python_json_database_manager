from __future__ import annotations

from user_storage.exceptions import UserAlreadyExists
from user_storage import BaseStorage
from python_json_database_manager import Database
from user import User
from contextlib import contextmanager

import uuid


class JsonUserStorage(BaseStorage):
	user_filename = "users"
	aliases_filename = "alias"
	
	users = Database("users")
	aliases = Database("aliases")
	
	def __init__(self):
		super().__init__()
		self.user_filename = JsonUserStorage.user_filename
		self.aliases_filename = JsonUserStorage.aliases_filename
		
		self.users = JsonUserStorage.users
		self.aliases = JsonUserStorage.aliases
	
	@staticmethod
	def create_storage_on_disk():
		""" Creates the database. If its already there it will not be touched """
		Database.create(JsonUserStorage.user_filename, {})
		Database.create(JsonUserStorage.aliases_filename, {})
	
	def create_user(self, user: User = None) -> User:
		"""
		Adds a user to the database. Will raise UserAlreadyExists if the user is already in the database
		
		if user is None a default empty user is made with a unique id
		if user is a string a default empty user is made with the string as id
		if user is a user object the data is used from the user object to create the user in the database
		:param user: object or user_id string
		"""
		
		if user is None:
			new_id = str(uuid.uuid4())
			new_user_data = {
				User._user_id_key: new_id,
				User._verified_key: False,
				User._verified_data_key: {},
				User._email_key: None
			}
			self.users.adds(new_id, new_user_data)
			return self.create_user_object(new_user_data)
		
		elif isinstance(user, str):
			if self.already_exits(user):
				raise UserAlreadyExists(user)
			
			user_id = User.get_id(user)
			
			# just add the id and required tags all being None except id defaults
			new_user_data = {
				User._user_id_key: user_id,
				User._verified_key: False,
				User._verified_data_key: {},
			}
			self.users.adds(user_id, new_user_data)
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
			}  # Enforce defaults
			
			self.users.adds(user.user_id, new_user_data)
			return self.create_user_object(new_user_data)
	
	def read_user(self, user: User, skip_aliases: bool = False) -> User:
		""" Reads and returns a user, can be string or user object """
		user_id = BaseStorage.get_id(user)
		try:
			user_data = self.users.translates(user_id)
		
		except KeyError as key_error:
			if skip_aliases:
				raise key_error
			new_user_id = JsonUserStorage.aliases.translates(user_id)
			user_data = JsonUserStorage.users.translates(new_user_id)
		
		return self.create_user_object(user_data)
	
	@staticmethod
	def update_user_key(user: User, new_key: str, check_for_alias: bool = False):
		"""
		Changes a the key a user is saved under
		:param user: The user object which key has to be changed. Can be string or user object
		:param new_key: The new key you want the user to be under
		:param check_for_alias: do you want to go trough the alias file and rename the old id to the new id
		
		:raise UserAlreadyExists
		"""
		old_user_id = User.get_id(user)
		
		if JsonUserStorage.already_exits(new_key):
			raise UserAlreadyExists(new_key)
		
		with JsonUserStorage.users as users:
			users[new_key] = user
			del users[old_user_id]
		
		if check_for_alias:
			JsonUserStorage.replace_alias(old_user_id, new_key)
	
	@staticmethod
	def replace_alias(old_alias: str, new_alias: str):
		"""
		Replaces an old alias with a new alias.
		The key will stay the same but the value the alias points to is changed.
		:param old_alias: The old alias value
		:param new_alias: The new alias value
		:return:
		"""
		with Database(JsonUserStorage.aliases_filename) as alias:
			if old_alias in alias.values():
				for key, value in alias:
					if value == old_alias:
						alias[key] = new_alias
	
	def update_user(self, user: User, new_user: User) -> User:
		"""
			Updates the user record
			The user given will replace the user in the database
		"""
		user_id = User.get_id(user)
		with self.users as users:
			users[user_id] = new_user
		return new_user
	
	def merge_user(self, user: User, new_user: User) -> User:
		""" Merges instead of replaces a user """
		user_id = User.get_id(user)
		with self.users as users:
			users[user_id] |= user
			new_data = users[user_id]
		return new_data
	
	def delete_user(self, user: User) -> User:
		"""" Deletes a user from the database """
		user_id = User.get_id(user)
		with JsonUserStorage.users as users:
			deleted_user = users[user_id]
			del users[user_id]
		return deleted_user
	
	@staticmethod
	def already_exits(user) -> bool:
		""" Returns true if the user is already found in the database :returns bool """
		user_id = User.get_id(user)
		if user_id in JsonUserStorage.users:
			return True
		else:
			try:
				translated_user_id = JsonUserStorage.aliases.translates(user_id)
				if translated_user_id in JsonUserStorage.users:
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
		if JsonUserStorage.already_exits(real_id):
			raise UserAlreadyExists(real_id, message=f"Can't use an id that already exists as an alias, id: {real_id}")
		Database.add(JsonUserStorage.aliases_filename, alias, real_id)
	
	@staticmethod
	def delete_alias(alias: str):
		"""
		Removes an alias from the alias json
		:param alternate_id:
		"""
		with JsonUserStorage.aliases as aliases:
			del aliases[alias]
	
	@contextmanager
	def yield_user_context(self, user: User) -> User:
		"""
		The context manages will merge the user again after the with.
		:param user:
		"""
		user_id = User.get_id(user)
		try:
			user_object = self.read_user(user_id)
			yield user_object
			self.merge_user(user_id, user_object)
			print("after merge")
		# except
		finally:
			print("finally")

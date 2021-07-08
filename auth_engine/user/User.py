from collections import UserDict

from user_storage import BaseStorage
import secrets

import re

email_regex = re.compile(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")


class User(UserDict):
	"""
	Object to represent users.
	Should be returned by storages
	Only if it gets a storage can it be verified
	"""
	_verified_key = "_verified"  # Key under which the verified status is stored in the user object
	_verified_data_key = "_verified_data"  # Key under which data for the verification process is stored
	_user_id_key = "_id"  # Key under which the id is stored in the user object
	_email_key = "email"  # Key under which the email s stored in hte user object
	
	def __init__(self, user_id: str, storage: BaseStorage = None, data: dict = None):
		"""
		If a storage is given the data is pulled from the storage,
		If no storage is given the data is pulled from the data dict
		
		The default data is added to the data if it
		Email key is not added as it not being there and raising a KeyError is better + there is a property
		that says if the user has an email.
		user_id is always added to the data. I can't imagine a senario that you wouldn't want that
		"""
		
		user_id = User.get_id(user_id)
		
		if data is None and storage is None:
			data = {User._user_id_key: user_id, User._verified_key: False, User._verified_data_key: {}}
		
		elif data is None and storage is not None:
			data = storage.read_user(user_id)
		
		# Add the id to the data
		data[User._user_id_key] = user_id
		
		# Add missing data
		if User._verified_data_key not in data:
			data[User._verified_data_key] = {}
		if User._verified_key not in data:
			data[User._verified_key] = False
		
		super().__init__(data)
		
		self.storage = storage
	
	@property
	def is_verified(self) -> bool:
		""" :returns true if the user is verified """
		return self.data[User._verified_key]
	
	@property
	def verified_data(self) -> dict:
		"""
		The verification data. You can store tokens and stuff here.
		Remeber dicts are passed by reference so you can just update it
		:return: dict
		"""
		return self.data[User._verified_data_key]
	
	@verified_data.setter
	def verified_data(self, new_data: dict):
		self.data[User._verified_data_key] = new_data
	
	@property
	def user_id(self) -> str:
		return str(self.data[User._user_id_key])
	
	@property
	def is_known(self) -> bool:
		""" Should returns True if the user id is known
		If there is no storage then it returns False
		:return: bool
		"""
		if not self.linked_to_storage:
			return False
		return self.user_id in self.storage
	
	@property
	def has_email(self) -> bool:
		if User._email_key in self.data:
			return True
		return False
	
	@property
	def email(self) -> str:
		return self.data[User._email_key]
	
	@email.setter
	def email(self, new_email) -> None:
		self.data[User._email_key] = new_email
	
	@property
	def linked_to_storage(self) -> bool:
		"""Returns true if self.storage is not None"""
		if self.storage is None or not isinstance(self.storage, BaseStorage):
			return False
		return True
	
	def sync_from_storage(self) -> None:
		"""
		Sync user data from the storage
		"""
		if not self.linked_to_storage:
			raise AttributeError("A user has to have a working storage connected to be synced.")
		self_from_storage = self.storage.read_user(self)
		self.data = self_from_storage.data
		
	def sync_to_storage(self) -> None:
		"""
		Sync a user to the storage
		"""
		if not self.linked_to_storage:
			raise AttributeError("A user has to have a working storage connected to be synced.")
		self.storage.merge_user(self, self)
	
	def verify(self) -> bool:
		if not self.linked_to_storage:
			raise AttributeError("A user has to have a working storage connected to be verified.")
		
		if self.is_verified:
			return True
		
		if self.has_email:
			raise KeyError("User needs to have email in account to be verified.")
		
		#  If not returned then the user is not verified and has an email so lets get going on that
		# with
		email = self.storage.read_user(self)[User._email_key]
		self.storage[self.user_id][User._verified_data_key]["token"] = secrets.token_urlsafe()
	
	@staticmethod
	def get_id(user) -> str:
		"""
		Give a user id or a string. If it gets a string it just returns the string
		If it gets a user object it returns the user id of the user
		If it gets something else it raises NotImplemented

		This has nothing to do with the aliases it just gives you certanty that you have the id
		:param user:
		:return: The user id
		"""
		if isinstance(user, str):
			return user
		elif isinstance(user, User):
			return user.user_id
		elif isinstance(user, dict):
			return user[User._user_id_key]
		else:
			raise NotImplementedError(f"get_id can only receive user objects or strings but got {user}")

	@property
	def has_valid_email(self) -> bool:
		if not self.has_email:
			return False
		if email_regex.fullmatch(self.email):
			return True
		return False
	
	def __repr__(self):
		return f"|User: {self.user_id}|"


class UnverifiedUser(Exception):
	def __init__(self, user: User, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"user {user} is not verified."
		super().__init__(message)
		
		self.user = user


class UnknownUser(Exception):
	""" Raised if we have an unknown user when we should have a known user """
	
	def __init__(self, user: User, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"user {user} is not known."
		super().__init__(message)
		self.user = user

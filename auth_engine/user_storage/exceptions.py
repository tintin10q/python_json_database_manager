from __future__ import annotations


class UserAlreadyExists(Exception):
	def __init__(self, user: User, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"user {user} already exists verified."
		super().__init__(message)
		
		self.user = user


class UserHasNoStorage(Exception):
	def __init__(self, user: User, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"user {user} has no working self.storage."
		super().__init__(message)
		
		self.user = user


class IdMixup(Exception):
	""" Raised if we have an unknown user when we should have a known user """
	
	def __init__(self, user: User, message=None, alternate_id: str = ""):
		if message is None:  # Always try to create the message trough the info
			message = f"user {user} is not consistant in their ids. {alternate_id}"
		super().__init__(message)
		self.user = user

from user import User
from user import UnknownUser, UnverifiedUser
from proofs.exceptions import InvalidProof


def can_user_recieve_passport(user: User) -> bool:
	"""
	Returns true if:
		if the user is known
		if the user is verified
	
	This could be just a method on the user but for now I am leaving it as a usecase because I don't like a property raising errors.
	And this would be more clear
	:param user:
	:return: bool
	:raises: UnkownUser, UnverifiedUser
	"""
	
	if not user.is_known:
		raise UnknownUser(user, f"Unkown user: {user} tried to get a passport, a user needs to have a storage to be known")
	
	if not user.is_verified:
		raise UnverifiedUser(user)
	
	return True

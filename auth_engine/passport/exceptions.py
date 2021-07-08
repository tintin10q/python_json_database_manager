
class MyError(Exception):
	def __init__(self, info, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"the info is {info}"
		super().__init__(message)
		
		self.info = info


class PassportWithEmptyClaims(Exception):
	"""
	Can be raised if a passport is tried to be created but the claims are empty
	"""
	def __init__(self, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"A passport was requested with an empty claim"
		super().__init__(message)
		

class ClaimIsNoClaimObject(Exception):
	"""
	You can raise this if it is not a Claim object
	"""
	
	def __init__(self, not_a_Claim, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"{not_a_Claim} object was not a Claim"
		super().__init__(message)
		
		self.not_a_claim = not_a_Claim




class TryingToAccessUnstampedPassport(Exception):
	"""
	Raised by the passport when your trying to access an unstammped passport
	"""
	
	def __init__(self, passport, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"{passport}'s passport was tried to accessed without being stamped"
		super().__init__(message)
		
		self.passport = passport

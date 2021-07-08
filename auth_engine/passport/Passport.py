
from claims import BaseClaims
from passport.exceptions import TryingToAccessUnstampedPassport



class Passport:
	"""
	A container object that stamp the claims into a passport
	You give the claims to the stamp method.
		
	"""
	
	def __init__(self):
		self.__claims = {}
		self.stamped = False
		self.__passport = ""
	
	@property
	def encoded_passport(self):
		"""The passport property holding the passport will only return if stamped"""
		if not self.stamped:
			raise TryingToAccessUnstampedPassport(self)
		return self.__passport
	
	@encoded_passport.setter
	def encoded_passport(self, new_passport):
		self.__passport = new_passport
	
	@property
	def claims(self):
		if not self.stamped:
			raise TryingToAccessUnstampedPassport(self)
		return self.__claims
	
	
	def remove_stamp(self):
		"""
			Removes stamp from passport.
			Does not really need to be overwritten.
		"""
		self.passport = None
		self.stamped = False
	
	def stamp(self, claims: BaseClaims):
		""" Method that should stamp the passport.	"""
		raise NotImplementedError
		
		new_passport = str(claims)  # First make the encoded passport
		self.stamped = True         # Stamp the passport
		self.encoded_passport = new_passport  # Save the passport in self.encoded_passport

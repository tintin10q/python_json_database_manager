import jwt
from enum import Enum

from claims import JwtClaims

from passport import Passport


class JwtPassport(Passport):
	"""Encodes the namespaced_claims into a jwt token"""
	
	def __init__(self, key: bytearray, algorithm: str):
		"""
		:param private_key: The private key of the jwt token. Should come from pem file or environment var.
		:param algorithm: The algorithm to use when encoding the token
		"""
		
		self.algorithm = algorithm
		self.__key = key
	
	def stamp(self, claims: JwtClaims):
		"""
		Stamps the passport with a jwt token based on the algorithm.
		:return:
		"""
		new_passport = jwt.encode(self.claims, self.__key, algorithm=self.algorithm)
		self.stamped = True
		self.encoded_passport = new_passport

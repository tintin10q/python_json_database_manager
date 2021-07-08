
from proofs import Proof
import bcrypt


class BcryptPasswordProof(Proof):
	"""This proof is valid if the password hashes to the hashed_password with bcrypt """
	
	def __init__(self, password: bytes, hashed_password: bytes):
		
		assert isinstance(password, bytes), "Password should be bytes"
		assert isinstance(hashed_password, bytes), "Hashed_password should be bytes"
		
		super().__init__()
		
		self.__password = password
		self.hashed_password = hashed_password
		
	@property
	def is_valid(self) -> bool:
		""" Check password """
		if self.invalidated:
			return False
		return bcrypt.checkpw(self.__password, self.hashed_password)

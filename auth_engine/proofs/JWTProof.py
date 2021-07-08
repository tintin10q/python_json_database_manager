from Proof import Proof
import jwt


# https://stackoverflow.com/questions/29650495/how-to-verify-a-jwt-using-python-pyjwt-with-public-key

class JWTProof(Proof):
	"""
	This proof checks if you can decode a jwt token with a given public key.

	I recommend the public key to be like this:
	from cryptography import serialization
	
	with open("mykey.pub", "rb") as key_file:
		public_key = serialization.load_pem_public_key(
			key_file.read(),
			backend=default_backend()
		)
		
	###algortims has to be one of :
		-
		-
		-
		
	"""
	
	def __init__(self, token: bytearray, public_key, algorithms: list[str] = "RS256"):
		super().__init__()
		self.jwt_token = token
		self.public_key = public_key
		self.algorithms = algorithms
		
	@property
	def is_valid(self):
		""" Decode jwt token """
		try:
			jwt.decode(self.jwt_token, self.public_key, algorithms=self.algorithms)
			return True
		except jwt.exceptions.DecodeError:
			# Maybe add more info like invalid because .....
			return False
	
	@property
	def claims(self):
		""" The namespaced_claims in the key"""
		return jwt.decode(self.jwt_token, self.public_key, algorithms=self.algorithms)

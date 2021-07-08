# coding=utf-8

from proofs import Proof


class TokenProof(Proof):
	"""
	This proof is valid if the given token is in a plaintext token file
	
	You can give the file name as an input but the default is VALID_TOKENS
	
	If you use this proof do not forget to put the filename you use in .gitignore
	
	This class will not create the VALID_TOKENS you have to make it yourself but there is a method
	called does_token_file_exist() which returns True or False depending on if the file exits
	
	The token file should just be a plain text file of tokens. Each line of the text file is considered a token.
	The token you give to __init__ should not have the lineline at the end! It is removed here!
	
	Empty lines in the token file are ignored. The token file is opend as encoding="utf-8".
	
	"""
	
	def __init__(self, token: str, token_filename: str = "VALID_TOKENS"):
		super().__init__()
		self.token = token
		self.token_filename = token_filename
	
	@property
	def is_valid(self) -> bool:
		""" Check if token is in file"""
		
		if self.invalidated:
			return False
		
		with open(self.token_filename, "r", encoding="utf-8") as token_file:
			for token in token_file:
				token = token.rstrip()  # remove \n and stuff from end of token
				if not token or len(token) == 0:
					continue
				
				if token == self.token:
					return True
		return False
	
	def does_token_file_exists(self) -> bool:
		"""
		Returns True if the token file exists
		:return: bool
		"""
		from os.path import exists
		
		if exists(self.token_filename):
			return True
		return False

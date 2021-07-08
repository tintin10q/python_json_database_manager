
class Proof:
	def __init__(self):
		self.__invalidated = False
	
	@property
	def is_valid(self):
		""" Is the proof valid or not """
		# Find out if proof is valid
		if self.invalidated:
			return False
		
		raise NotImplementedError
	
	def __bool__(self):
		return self.is_valid
	
	def make_invalid(self):
		self.__invalidated = True
	
	@property
	def invalidated(self):
		return self.__invalidated


class CashedProof:
	""" This proof saves if the proof is valid after trying once. Retry with .retry()"""
	
	def __init__(self, proof: Proof):
		super().__init__()
		self.__valid = None
		self.proof = proof
	
	@property
	def is_valid(self):
		""" Is the proof valid or not? Cashes result of that question! """
		if self.__valid is None:
			self.__valid = self.proof.is_valid  # Find out if proof is valid
			return self.__valid
		else:  # Return
			return self.__valid
	
	def __bool__(self):
		return self.__valid
	
	def refresh(self):
		self.__valid = self.proof.is_valid

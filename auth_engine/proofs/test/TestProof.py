from proofs import Proof


class TestProof(Proof):
	"""
	Test proof for testing
	"""
	def __init__(self):
		super().__init__()
		self._valid = False
		
	@property
	def is_valid(self):
		""" Is the proof valid or not """
		# Find out if proof is valid
		if self.invalidated:
			return False
		
		return self._valid
	
	def __bool__(self):
		return self.is_valid

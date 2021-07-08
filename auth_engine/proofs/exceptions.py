from proofs.Proof import Proof

class MyError(Exception):
	def __init__(self, info, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"the info is {info}"
		super().__init__(message)
		
		self.info = info


class InvalidProof(Exception):
	def __init__(self, proof: Proof, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"{proof} is now invalid"
		super().__init__(message)
		
		self.proof = proof

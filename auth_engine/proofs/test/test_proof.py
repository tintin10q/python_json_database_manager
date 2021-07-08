import unittest


from TestProof import TestProof


proof_to_test =  TestProof
proof_arguments = {}

class TestProof(unittest.TestCase):
	def test___bool__(self):
		proof = proof_to_test()
		if proof:
			pass
		if not proof:
			pass
	
	def test_is_valid(self):
		proof = proof_to_test()
		self.assertEqual(proof.is_valid, False)
		proof._valid = True
		self.assertEqual(proof.is_valid, True)
		proof._valid = False
		self.assertEqual(proof.is_valid, False)
		proof._valid = True
		self.assertEqual(proof.is_valid, True)

		
	def test_proof_invalidation(self):
		proof = proof_to_test()
		proof._valid = True
		self.assertEqual(proof.is_valid, True)
		proof.make_invalid()
		self.assertEqual(proof.is_valid, False)
		
if __name__ == '__main__':
	unittest.main()

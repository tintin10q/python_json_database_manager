import unittest
from claims import TimedClaims

class TestTimedClaims(unittest.TestCase):
	
	my_claims = {"global_username": "quinten"}
	
	def setUp(self, global_claims: dict = None, valid_time: int = 100000) -> None:
		
		if global_claims is None:
			global_claims = TestTimedClaims.my_claims
		
		self.global_claims = global_claims
		self.valid_time = valid_time
		self.test_claim = TimedClaims(self.global_claims, valid_time)
	
	def test_claim_in_data(self):
		self.setUp(global_claims=TestTimedClaims.my_claims)
		self.assertIn("global_username", self.test_claim)
		self.assertEqual(self.test_claim["global_username"], "quinten")
	
	def test_is_exp_in_data(self):
		self.assertIn("exp", self.test_claim)
		
	def test_is_iat_in_data(self):
		self.assertIn("iat", self.test_claim)
	
	def test_if_exp_is_float(self):
		self.assertTrue(isinstance(self.test_claim["exp"], float))
		
	def test_if_iat_is_float(self):
		self.assertTrue(isinstance(self.test_claim["iat"], float))
		
if __name__ == '__main__':
	unittest.main()

import unittest

from claims import JwtClaims, TimedJwtClaims
from claims.test import TestNamespacedClaim, TestTimedClaims


class TestJwtClaim(TestNamespacedClaim):
	
	def setUp(self, namespace: str = "https://test_namespace.gg", namespaced_claims=None) -> None:
		TestNamespacedClaim.setUp(self, namespace, namespaced_claims)
		self.test_claim = JwtClaims(self.namespace, self.namespaced_claims, "sub", "aud", "iss")
	
	def test_iss_in_data(self):
		self.assertIn("iss", self.test_claim)
		self.assertEqual(self.test_claim["iss"], "iss")
	
	def test_aud_in_data(self):
		self.assertIn("aud", self.test_claim)
		self.assertEqual(self.test_claim["aud"], "aud")
	
	def test_sub_in_data(self):
		self.assertIn("sub", self.test_claim)
		self.assertEqual(self.test_claim["sub"], "sub")


class TestTimedJwtClaims(TestJwtClaim, TestTimedClaims):
	
	def setUp(self, namespace: str = "test_namespace", namespaced_claims: dict = None, global_claims: dict = None, valid_time: int = 100000) -> None:
		TestJwtClaim.setUp(self, namespace, namespaced_claims)
		TestTimedClaims.setUp(self, global_claims, valid_time)
		
		self.test_claim = TimedJwtClaims(namespace=self.namespace, namespaced_claims=self.namespaced_claims,
		                                 sub="sub", aud="aud", iss="iss",
		                                 valid_seconds=self.valid_time, global_claims=self.global_claims)
	
	def test_exstra_full_assertEqual(self):
		self.assertIn("aud", self.test_claim)
		self.assertIn("exp", self.test_claim)
		self.assertIn("iat", self.test_claim)
		self.assertIn("iss", self.test_claim)
		self.assertIn("nfb", self.test_claim)
		self.assertIn("sub", self.test_claim)
		for key in self.global_claims.keys():
			self.assertIn(key, self.test_claim)
		self.assertIn(*self.global_claims.keys(), self.test_claim.keys())
		self.assertTrue(isinstance(self.test_claim[self.namespace], dict))
		
	
if __name__ == '__main__':
	unittest.main()

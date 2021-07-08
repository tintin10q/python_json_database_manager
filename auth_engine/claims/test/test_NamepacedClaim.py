import unittest

from claims import NamespacedClaim


class TestNamespacedClaim(unittest.TestCase):
	
	def setUp(self, namespace: str = "https://test_namespace_from_TestNamespacedClaim.gg", namespaced_claims=None) -> None:
		
		if namespaced_claims is None:
			namespaced_claims = {"name": "quinten", "id": 137}
			
		self.namespaced_claims = namespaced_claims
		self.namespace = namespace
		self.test_claim = NamespacedClaim(self.namespace, self.namespaced_claims)
		
	def test_namespace_is_made(self):
		self.assertIn(self.namespace, self.test_claim)
	
	def test_namespace_has_given_claims(self):
		self.assertEqual(self.test_claim[self.namespace], self.namespaced_claims)

	def test_raises_ValueError_with_too_long_namespace(self):
		ok_namespacename = "q" * 256
		too_long_namespacename = "q" * 257
		
		# can make namespace with 256 long without error
		self.setUp(namespace=ok_namespacename)
		
		with self.assertRaises(ValueError):
			self.setUp(namespace=too_long_namespacename)
		
if __name__ == '__main__':
	unittest.main()

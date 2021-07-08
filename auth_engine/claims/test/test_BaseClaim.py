import unittest

from claims.BaseClaim import BaseClaims


class BaseClaimTest(unittest.TestCase):
	
	def test_no_arguments_gives_empty_dict(self):
		claims = BaseClaims()
		self.assertEqual(claims, {})
	
	def test_claims_dict_input(self):
		claims_input = {"Username": "test", 'hoi': 3}
		claims = BaseClaims(claims_input)
		self.assertEqual(claims, claims_input)
	
	def test_base_claim_str(self):
		claims = BaseClaims({"HI": "test", 'hoi': 3})
		self.assertEqual(claims.__repr__(), str({"HI": "test", 'hoi': 3}))
	
	def test_adding_claims_dict(self):
		claims_input = {"Username": "test", 'hoi': 3}
		claims_added = {"name": "test"}
		expected_result = {"Username": "test", "name": "test", 'hoi':3 }
		claims = BaseClaims(claims_input)
		claims |= claims_added
		self.assertEqual(claims, expected_result)
	
	def test_adding_claims_other_claim_object(self):
		claims_input = {"Username": "test", 'hoi': 3}
		claims_input2 = {"Username2": "test2", 'hoi2': 5}
		expected_result = {"Username": "test", 'hoi': 3, "Username2": "test2", 'hoi2': 5}
		claims = BaseClaims(claims_input)
		new_claims = BaseClaims(claims_input2)
		claims |= new_claims
		self.assertEqual(claims, expected_result)
	
	def test_claims_setter(self):
		claims = BaseClaims()
		claims.update({"a": "a", "b": "b"})
		self.assertEqual(claims, {"a": "a", "b": "b"})
		
		claims = BaseClaims()
		claims.data = {"a": "a", "b": "b"}
		self.assertEqual(claims, {"a": "a", "b": "b"})
		
		claims = BaseClaims({"test":"aapje"})
		claims |= {"a":"a","b":"b"}
		self.assertEqual(claims, {"a":"a","b":"b","test":"aapje"})
		
		
if __name__ == '__main__':
	unittest.main()


	abc = {
		"a": "b",
		"b": "c",
		"c": "a"
	}

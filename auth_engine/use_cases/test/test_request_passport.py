import unittest


from use_cases.request_passport import request_passport

from claims.BaseClaim import BaseClaims
from claims import BaseClaims
from proofs import InvalidProof, Proof
from user import User, UnverifiedUser, UnknownUser

class RequestPasswordUsecase(unittest.TestCase):
	def test_user_input_has_to_be_user_object(self):
		
		with self.assertRaises(AssertionError):
			password = request_passport(1,2)
			password = request_passport(3,3)
			password = request_passport("s", "s")
		
	def test_raises_UnkownUser(self):
		pass

if __name__ == '__main__':
	unittest.main()

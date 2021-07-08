import unittest
from proofs import BcryptPasswordProof
import bcrypt


class TestBcryptPassword(unittest.TestCase):
	def test_valid_hash(self):
		"""Test if the proof is valid with a valid password"""
		password = b"bad_password"
		salt = bcrypt.gensalt(5)
		hashed_password = bcrypt.hashpw(password, salt)
		proof = BcryptPasswordProof(password, hashed_password)
		
		self.assertEqual(proof.is_valid, True)

	def test_invalid_hash(self):
		"""Test if the proof is invalid with a wrong password"""
		password = b"bad_password"
		salt = bcrypt.gensalt(5)
		hashed_password = bcrypt.hashpw(password, salt)
		
		proof = BcryptPasswordProof(password+b"a", hashed_password)
		self.assertEqual(proof.is_valid, False)
		
	def test_invalidated(self):
		"""Test if the proof can be invalidated"""
		password = b"bad_password"
		salt = bcrypt.gensalt(5)
		hashed_password = bcrypt.hashpw(password, salt)
		proof = BcryptPasswordProof(password, hashed_password)
		self.assertEqual(proof.is_valid, True)
		
		proof.make_invalid()
		
		self.assertEqual(proof.is_valid, False)


if __name__ == '__main__':
	unittest.main()

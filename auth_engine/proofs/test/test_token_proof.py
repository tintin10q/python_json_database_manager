# encoding=utf-8

import unittest
from proofs import TokenProof
from os import remove


class TestTokenProof(unittest.TestCase):
	token_filename = "TEST_VALID_TOKENS.txt"
	
	def setUp(self, valid_tokens=None) -> None:
		"""Create a token file before the test"""
		if valid_tokens is None:
			valid_tokens = ["hi_there\n", "VALID_TOKEN\n", "aaa\n", "\n", "1234\n"]
		self.valid_tokens = valid_tokens
		self.valid_token = "VALID_TOKEN"
		self.invalid_token = "INVALIDTOKEN!!!!"
		
		with open(TestTokenProof.token_filename, "w+", encoding="utf-8") as test_valid_tokens:
			test_valid_tokens.writelines(self.valid_tokens)
		
		# Validate if the file is fine:
		found_valid_token = False
		found_invalid_token = False
		self.found_empty_token = False
		
		with open(TestTokenProof.token_filename, "r", encoding="utf-8") as tokensfile:
			for token in tokensfile:
				token = token.rstrip()
				if token == self.valid_token:
					found_valid_token = True
				if token == self.invalid_token:
					found_invalid_token = True
			
			assert not found_invalid_token, f"The test setup is invalid. self.invalid_token ({self.invalid_token}) token is in valid_tokens"
			assert found_valid_token, f"The test setup is invalid. Valid token is not in valid_tokens. Make sure you include {repr(self.valid_token)} in the tokens with a \\n at the end"
	
	def tearDown(self) -> None:
		"""Remove the token file after the test"""
		remove(TestTokenProof.token_filename)
	
	def test_valid_token(self):
		"""Tests if a valid token will give a valid proof"""
		proof = TokenProof(self.valid_token, TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, True)
	
	def test_unvalid_token(self):
		"""This test tests if an unvalid token will give an unvalid proof"""
		proof = TokenProof(self.invalid_token, TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False)
	
	def test_ignore_empty_token(self):
		r"""Tests if an empty token will pass. IT SHOULD NOT. Having empty lines is too risky. Caused by having \n
			in the token file. This test tests with or without having the empty line in the token file.
		"""
		self.setUp(["VALID_TOKEN\n", "\n", "  \n", "   \n", "last token\n"])
		proof = TokenProof("", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False)
		proof = TokenProof("   ", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False)
		
		self.setUp(["VALID_TOKEN\n", "last token"])
		proof = TokenProof("", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False)
	
	def test_weird_tokens_there(self):
		"""Tests weird tokens when they are in the token file"""
		self.setUp(["VALID_TOKEN\n", "\n", "\n\n","\t\n", "€\n", "aa\t\n","\ta\n", "a😀😀😀b😀 \n"])
		
		proof = TokenProof("\n", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False) # should always fail
		
		proof = TokenProof("€", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, True)
		
		proof = TokenProof("a😀😀😀b😀", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, True)
		
		proof = TokenProof("\t", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False) # should still fail because its removed
	
		proof = TokenProof("aa\t", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False) # this fails because?
		
		proof = TokenProof("\ta", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, True) # only space at the end is removed
	
	def test_weird_tokens_not_there(self):
		"""Test some weird tokens if they are not in the token file """
		proof = TokenProof("\n", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False)
		
		proof = TokenProof("€", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False)
		
		proof = TokenProof("😀😀😀😀", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False)
		
		proof = TokenProof("\t", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False)
		
		proof = TokenProof("\t", TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, False)
	
	def test_invalidated_proof(self):
		"""Test if the proof can be invalidated"""
		proof = TokenProof(self.valid_token, TestTokenProof.token_filename)
		self.assertEqual(proof.is_valid, True)
		proof.make_invalid()
		self.assertEqual(proof.is_valid, False)

	

if __name__ == '__main__':
	unittest.main()

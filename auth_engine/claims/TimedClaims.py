from claims import BaseClaims

import time


class TimedClaims(BaseClaims):
	def __init__(self, global_claims: dict, valid_seconds: int, valid_after_seconds=0):
		
		BaseClaims.__init__(self)
		
		now = time.time()
		self.data["iat"] = now
		self.data["exp"] = now + valid_seconds
		self.data["nfb"] = now + valid_after_seconds
		self.data |= global_claims

"""

exp (expiration time): Time after which the JWT expires

nbf (not before time): Time before which the JWT must not be accepted for processing

iat (issued at time): Time at which the JWT was issued; can be used to determine age of the JWT

"""

from claims import util

from claims import TimedClaims, NamespacedClaim


class JwtClaims(NamespacedClaim):
	def __init__(self, namespace: str, namespaced_claims: dict, sub: str, aud: str, iss: str):
		"""
		This is a claim that has the basic jwt claims
		:param namespaced_claims: the claims that go into the namespace
		:param namespace: the name of the namespace that the claims will go into
		:param sub: (subject): Subject of  the JWT (the user)
		:param aud: (audience): Recipient for which the JWT is intended
		:param iss: (issuer): Issuer of the JWT
		"""
		
		super().__init__(namespace, namespaced_claims)
		
		self.data["sub"] = sub
		self.data["aud"] = aud
		self.data["iss"] = iss


# This works nice now namespace could also be a class with multiple namespaces in one StandartClaims

class TimedJwtClaims(TimedClaims, JwtClaims):
	
	def __init__(self, namespace: str, namespaced_claims: dict, sub: str, aud: str, iss: str, valid_seconds, valid_after_seconds: int = 0, global_claims: dict = None):
		"""
		
		:param namespace: the namespace that the namespaced_claims go into
		:param namespaced_claims: the claims that go into the namespace
		:param sub: (subject): Subject of  the JWT (the user)
		:param aud: (audience): Recipient for which the JWT is intended
		:param iss: iss: (issuer): Issuer of the JWT
		:param valid_seconds: amount of seconds jwt should be valid
		:param valid_after_seconds: amount of seconds to wait before ativating the jwt
		:param global_claims: claims dict that should go on the top level of the jwt
		"""
		if global_claims is None:
			global_claims = {}
		
		JwtClaims.__init__(self, namespace, namespaced_claims, sub, aud, iss)
		TimedClaims.__init__(self, global_claims, valid_seconds, valid_after_seconds)

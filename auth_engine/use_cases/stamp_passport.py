from proofs import Proof
from proofs.exceptions import InvalidProof
from passport import Passport
from claims import BaseClaims


def stamp_passport(passport: Passport, proof: Proof, claims: BaseClaims) -> Passport:
	"""
	Encodes the claims into the passport if the proof is valid
	
	:param proof: If the proof is valid the passport will be stamped with the claims
	:param claims: The claims that go into the passport
	:param passport: The passport to be stamped
	:return: Passport
	"""
	if proof.is_valid:
		passport.stamp(claims)
		return passport
	else:
		raise InvalidProof(proof)

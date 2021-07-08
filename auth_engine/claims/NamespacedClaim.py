from claims import BaseClaims


class NamespacedClaim(BaseClaims):
	"""
	A Claims that that puts the namespaced_claims under a namespace.
	The namespace should not be longer then 256.
	"""
	
	def __init__(self, namespace: str, namespaced_claims: dict = None, *args, **kwargs):
		
		if len(namespace) > 256:
			raise ValueError("Namespace length can not be longer than 256 characters")
		
		if namespaced_claims is None:
			namespaced_claims = {}
		
		super(BaseClaims, self).__init__()
		
		self.namespace = namespace
		self.namespaced_claims = namespaced_claims
		self.data.update({self.namespace: {**self.namespaced_claims}})

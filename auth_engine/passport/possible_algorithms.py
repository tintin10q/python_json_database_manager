"""
Possible algortims:
	HS256 - HMAC using SHA-256 hash algorithm (default)
	HS384 - HMAC using SHA-384 hash algorithm
	HS512 - HMAC using SHA-512 hash algorithm
	ES256 - ECDSA signature algorithm using SHA-256 hash algorithm
	ES256K - ECDSA signature algorithm with secp256k1 curve using SHA-256 hash algorithm
	ES384 - ECDSA signature algorithm using SHA-384 hash algorithm
	ES512 - ECDSA signature algorithm using SHA-512 hash algorithm
	RS256 - RSASSA-PKCS1-v1_5 signature algorithm using SHA-256 hash algorithm
	RS384 - RSASSA-PKCS1-v1_5 signature algorithm using SHA-384 hash algorithm
	RS512 - RSASSA-PKCS1-v1_5 signature algorithm using SHA-512 hash algorithm
	PS256 - RSASSA-PSS signature using SHA-256 and MGF1 padding with SHA-256
	PS384 - RSASSA-PSS signature using SHA-384 and MGF1 padding with SHA-384
	PS512 - RSASSA-PSS signature using SHA-512 and MGF1 padding with SHA-512
	EdDSA - Ed25519 signature using SHA-512. Provides 128-bit security
"""

possible_algoritms = [
	"HS256",
	"HS384",
	"HS512",
	"ES256",
	"ES256K",
	"ES384",
	"ES512",
	"RS256",
	"RS384",
	"RS512",
	"PS256",
	"PS384",
	"PS512",
	"EdDSA", ]

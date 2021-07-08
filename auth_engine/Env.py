from os import environ

environ["hi"] = "hi"
print(environ.get("hi"))

class NamespaceAlreadyDefinedInEnvorinment(Exception):
	def __init__(self):
		super().__init__()

def load_env_file(namespace="auth") -> environ:
	if namespace:
		...
	
# Some things loaded from namespace is a good idea like iss

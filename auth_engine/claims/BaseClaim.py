
# Maybe should be inherited from dict??

from collections import UserDict



class BaseClaims(UserDict):
	"""The most basic Claim class that every other claim class should be inherited from.
		Its just a dict but you can add more stuff if you want
	"""

	def __init__(self, *args, **kwargs):
		if hasattr(self, 'data'):
			return
		super().__init__(*args, **kwargs)

	def __delitem__(self, key):
		value = self.data.pop(key)
		self.data.pop(value, None)
	
	def __setitem__(self, key, value):
		if key in self:
			del self[self[key]]
		self.data[key] = value

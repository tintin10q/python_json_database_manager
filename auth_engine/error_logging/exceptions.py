


class MyError(Exception):
	def __init__(self, info, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"the info is {info}"
		super().__init__(message)
		
		self.info = info


class MyError(Exception):
	def __init__(self, info, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"the info is {info}"
		super().__init__(message)
		
		self.info = info


class MyError(Exception):
	def __init__(self, info, message=None):
		if message is None:  # Always try to create the message trough the info
			message = f"the info is {info}"
		super().__init__(message)
		
		self.info = info

def is_number(potential_number):
	"""
	Checks if an object is a number
	:param potential_number:
	:return bool:
	"""
	try:
		int(potential_number)
		return True
	except BaseException:
		return False

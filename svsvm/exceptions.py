from .constants import BASE_URL

class InvalidUserError(Exception):
	def __init__(self, message="Invalid Userid or Password!"):
		self.message = message
		super().__init__(self.message)

	pass

class RequestException(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)

	pass

class ValidationFailed(Exception):
	def __init__(self, message=None):
		if (message is None):
			self.message = f"Invalid Viewstate and/or Event Validation!\nUpdate them from {BASE_URL}"
		else:
			self.message = message
		super().__init__(self.message)

	pass

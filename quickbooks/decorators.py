from quickbooks.models import ResponseError

def catch_errors(func):
	def inner(request):
		try:
			return func(request)
		except Exception as e:
			ResponseError.log_error(request, e)
			raise e
	return inner

import xmlrpc.server
import xmlrpc.client
import sys


def check_if_integer_is_within_python_range(integer):
	if integer < -1 * sys.maxsize or integer > sys.maxsize:
		sys.stdout.write("\nTriggering a Stack Overflow because int is not within range.\n")
		raise ValueError("Triggering a Stack Overflow because integer isn't within the simulated size.")


class CalculatorServer:
	def __init__(self):
		self._srv = xmlrpc.server.SimpleXMLRPCServer(('localhost', 8080))
		self._srv.register_instance(self)
		self._srv.register_introspection_functions()
		# Register the methods below as XML-RPC methods
		self._srv.register_function(self.add, 'add')
		self._srv.register_function(self.subtract, 'subtract')
		self._srv.register_function(self.multiply, 'multiply')
		self._srv.register_function(self.divide, 'divide')
		self._srv.register_function(self.modulo, 'modulo')

	def start_server(self):
		sys.stdout.write("Running server on localhost:8080\n")
		self._srv.serve_forever()

	# Add - a method to take 0 to any number of parameters and return the sum of the parameters
	#  "add" with 0 parameters should return 0, "add" with 1 parameter should return the parameter
	def add(self, *args):
		try:
			# Check if all arguments are within the range
			for arg in args:
				check_if_integer_is_within_python_range(arg)
			temp_sum = sum(args)
			check_if_integer_is_within_python_range(temp_sum)
			return temp_sum
		except Exception:   # Handling server side errors
			return xmlrpc.client.Fault(3, "illegal argument type")

	# Subtract - a method that takes two parameters and returns the difference of the parameters
	def subtract(self, a, b):
		try:
			# Check if all arguments are within the range
			check_if_integer_is_within_python_range(a)
			check_if_integer_is_within_python_range(b)
			difference = a - b
			check_if_integer_is_within_python_range(difference)
			return difference
		except Exception:
			return xmlrpc.client.Fault(3, "illegal argument type")

	# Multiply - a method that takes zero to any number of parameters and returns the product of the parameters.
	#  "multiply" with 0 parameters should return 1, "multiply" with 1 parameter should return the parameter, otherwise
	#  it should return the product of all the parameters
	def multiply(self, *args):
		try:
			result = 1
			for arg in args:
				# Check if all arguments are within the range
				check_if_integer_is_within_python_range(arg)
				result *= arg
				check_if_integer_is_within_python_range(result)
			return result
		except Exception:
			return xmlrpc.client.Fault(3, "illegal argument type")

	# Divide - a method that takes two parameters and returns the quotient of the parameters
	#  If the second parameter is a 0, return a faultcode of 1 and a faultstring of "Attempt to divide by zero"
	def divide(self, a, b):
		try:
			if b == 0:
				return xmlrpc.client.Fault(1, "Attempt to divide by zero")
			# Check if all arguments are within the range
			check_if_integer_is_within_python_range(a)
			check_if_integer_is_within_python_range(b)
			dividend = a / b
			check_if_integer_is_within_python_range(dividend)
			return dividend
		except Exception:
			return xmlrpc.client.Fault(3, "illegal argument type")

	# Modulo - a method that takes two parameters and returns one parameter modulo the other.
	#  If the second parameter is a 0, return a faultcode of 1 and a faultstring of "Attempt to divide by zero"
	def modulo(self, a, b):
		try:
			if b == 0:
				return xmlrpc.client.Fault(1, "Attempt to divide by zero")
			# Check if all arguments are within the range
			check_if_integer_is_within_python_range(a)
			check_if_integer_is_within_python_range(b)
			modulus = a % b
			check_if_integer_is_within_python_range(modulus)
			return modulus
		except Exception:
			return xmlrpc.client.Fault(3, "illegal argument type")

	# Create a method to return 404 for any URL other than "/RPC"
	def _dispatch(self, method, params):
		if method != "RPC":
			return xmlrpc.client.Fault(404, "Not Found")
		return self._srv._dispatch(method, params)

	# Create a method to return 405 for any option other than "POST"
	def _marshaled_dispatch(self, data, dispatch_method=None, path=None):
		if dispatch_method != "POST":
			return xmlrpc.client.Fault(405, "Method Not Allowed")
		return self._srv._marshaled_dispatch(data, dispatch_method, path)


if __name__ == '__main__':
	try:
		srv = CalculatorServer()
		srv.start_server()
	except KeyboardInterrupt:
		sys.stdout.write("\nExiting...\n")
		sys.exit(0)

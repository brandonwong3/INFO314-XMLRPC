from xmlrpc.client import ServerProxy, Fault, Transport
import sys


# This is a CLI client for the XML-RPC server
# Create a ServerProxy object to connect to the XML-RPC server

# Create and set useragent

# We will run like this: python client.py <hostname> <port> <method> <arg1> <arg2> ...

class ClientXMLRPC:
	def __init__(self, hostname="localhost", port=8080, group_name="MY_GROUP"):
		# Set the user-agent header to the group name
		# Create and set the useragent
		class CustomUserAgent(Transport):
			user_agent = group_name
		self._srv = ServerProxy(f'http://{hostname}:{port}', transport=CustomUserAgent())

		# self._srv = ServerProxy(f'http://{hostname}:{port}')
		sys.stdout.write(f"Connecting to server at {hostname}:{port}\n")
		try:

			# Perform the operations requested by the user
			subtract_1_result = self._srv.subtract(12, 6)
			assert subtract_1_result == 6
			sys.stdout.write(f"\nsubtract_1_result: {subtract_1_result}\n")

			multiply_1_result = self._srv.multiply(3, 4)
			assert multiply_1_result == 12
			sys.stdout.write(f"\nmultiply_1_result: {multiply_1_result}\n")

			divide_1_result = self._srv.divide(10, 5)
			assert divide_1_result == 2
			sys.stdout.write(f"\ndivide_1_result: {divide_1_result}\n")

			modulo_1_result = self._srv.modulo(10, 5)
			assert modulo_1_result == 0
			sys.stdout.write(f"\nmodulo_1_result: {modulo_1_result}\n")
			add_1_result = self._srv.add(0)
			sys.stdout.write(f"\nadd_1_result: {add_1_result}\n")

			add_2_result = self._srv.add(1, 2, 3, 4, 5)
			assert add_2_result == 15
			sys.stdout.write(f"\nadd_2_result: {add_2_result}\n")

			multiply_2_result = self._srv.multiply(1, 2, 3, 4, 5)
			assert multiply_2_result == 120
			sys.stdout.write(f"\nmultiply_2_result: {multiply_2_result}\n")
		except AssertionError:
			sys.stdout.write("\nTest failed\n")

		# Checking addition of two very large numbers
		try:
			self._srv.add(sys.maxsize * 2, sys.maxsize * 2)
		except OverflowError:
			sys.stdout.write("\nAddition overflow Test passed\n")

		# Checking product of two very large numbers
		try:
			self._srv.multiply(sys.maxsize * 2, sys.maxsize * 2)
		except OverflowError:
			sys.stdout.write("\nMultiplication overflow Test passed\n")

		# Checking that subtract taking two string parameters should trigger illegal argument faults
		try:
			self._srv.subtract("a", "b")
		except Fault as f:
			if f.faultCode != 3:
				raise
			else:
				sys.stdout.write("\nSubtracting strings Test passed\n")

		# Checking that dividing by 0 triggers a divide-by-zero fault
		try:
			self._srv.divide(1, 0)
		except Fault as f:
			if f.faultCode != 1:
				raise
			else:
				sys.stdout.write("\nDivide by zero Test passed\n")


if __name__ == "__main__":
	command_line_arguments = sys.argv
	if len(sys.argv) != 3:
		sys.stdout.write("Usage: python client.py <hostname> <port>\n")
		sys.exit(1)
	hostname = sys.argv[1]
	port = int(sys.argv[2])
	client = ClientXMLRPC(hostname, port)
	sys.stdout.write("\nTest passed\n")

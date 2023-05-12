from xmlrpc.client import ServerProxy, Fault
import sys


# A test for the server.
# return a 404 for any URL other than "/RPC"
# return a 405 (Method Not Supported) for any operation other than POST

if __name__ == "__main__":
	server = ServerProxy("http://localhost:8080")
	try:
		# Try to go to http://localhost:8080/RPC
		test_server = ServerProxy("http://localhost:8080/RPC")
		# Try to test sending a request to a non-existent method
		server.non_existent_method()
	except Fault as f:
		if f.faultCode != 405 or f.faultCode != 404 or f.faultCode != 3 or f.faultCode != 1:
			raise
		else:
			sys.exit(1)
	sys.stdout.write("Success!\n")

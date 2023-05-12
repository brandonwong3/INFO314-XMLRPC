from xmlrpc.client import ServerProxy, Fault
import sys


# A test for the server.
# return a 404 for any URL other than "/RPC"
# return a 405 (Method Not Supported) for any operation other than POST

if __name__ == "__main__":

	try:
		server = ServerProxy("http://localhost:9090")
		result = server.anAction("test")
		print(result)
	except Fault as f:
		if f.faultCode != 405 or f.faultCode != 404 or f.faultCode != 3 or f.faultCode != 1:
			raise
		else:
			sys.exit(1)
	sys.stdout.write("Success!\n")

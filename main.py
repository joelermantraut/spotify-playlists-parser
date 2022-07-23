from credentials import Credentials
from arg_parsing import ArgParsing

def main():
	print("LOGGING\n")

	credentials = Credentials("data/.credentials")
	token = credentials.enter()

	if not(token):
		print("Failure on access")
		exit(1)

	# Logging, not change

	argparser = ArgParsing(token)

if __name__ == "__main__":
	main()
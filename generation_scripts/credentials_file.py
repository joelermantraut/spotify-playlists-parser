"""
Script to generate credentials file.
"""

def main():
	CREDENTIALS_FILEPATH = "data/.credentials"

	USERNAME = ""
	CLIENT_ID = ""
	CLIENT_SECRET = ""
	REDIRECT_URI = ""
	SCOPE = ""

	with open(CREDENTIALS_FILEPATH, "w") as file:
		file.write(f"{USERNAME},{CLIENT_ID},{CLIENT_SECRET},{REDIRECT_URI},{SCOPE}")

if __name__ == "__main__":
	main()
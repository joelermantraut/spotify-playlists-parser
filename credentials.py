"""
Class to read and decode credentials file, to log user to Spotify.
"""

import spotipy.util as util

class Credentials:
	"""
	Class that logs user to Spotify.
	"""
	def __init__(self, credentials_file):
		self.CREDENTIALS_FILE = credentials_file
		self.get_credentials()

	def get_credentials(self):
		with open(self.CREDENTIALS_FILE, "r") as file:
			content = file.read().split(",")

		self.username = content[0]
		self.clientid = content[1]
		self.clientsecret = content[2]
		self.redirecturi = content[3]
		self.scope = content[4]
		# Gets credentials from a file

	def enter(self):
		self.token = util.prompt_for_user_token(
			self.username,
			scope=self.scope,
			client_id=self.clientid,
			client_secret=self.clientsecret,
			redirect_uri=self.redirecturi
		)

		return self.token

if __name__ == "__main__":
	print("Logging\n")

	credentials = Credentials(".credentials")
	token = credentials.enter()

	if not(token):
		print("Failure on access")
		exit(1)

	print(token)
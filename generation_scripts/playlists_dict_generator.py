"""
Script to generate playlist dict and save it to a file, 
to after recover it in main script.
"""

import pickle

playlists = {

}

def main():
	PLAYLIST_FILEPATH = "../data/playlists.pkl"

	with open(PLAYLIST_FILEPATH, "wb") as file:
		pickle.dump(playlists, file)

if __name__ == "__main__":
	main()
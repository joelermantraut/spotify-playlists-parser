"""
Structure:

playlists = sp.playlist(playlist_id):
	'collaborative'
	'description'
	'external_urls'
	'followers'
	'href'
	'id'
	'images'
	'name'
	'owner'
	'primary_color'
	'public'
	'snapshot_id',
	'tracks'
	'type'
	'uri'

tracks = playlists["tracks"]:
	'href'
	'items'
	'limit'
	'next'
	'offset'
	'previous'
	'total'

songs = tracks["items"] # Almacena las canciones
first_song = songs[0]
	'added_at'
	'added_by'
	'is_local'
	'primary_color'
	'track'
	'video_thumbnail'

song_properties = first_song["track"]:
	'album'
	'artists'
	'available_markets'
	'disc_number'
	'duration_ms'
	'episode'
	'explicit'
	'external_ids'
	'external_urls'
	'href'
	'id'
	'is_local'
	'name'
	'popularity'
	'preview_url'
	'track'
	'track_number'
	'type'
	'uri'
"""

import spotipy
import pickle
import random

class parsePlaylists:
	"""
	Class that parses playlists, generating songs lists.
	"""
	def __init__(self, token, use_cache=False):
		self.token = token
		self.use_cache = use_cache
		self.PLAYLIST_FILEPATH = "data/playlists.pkl"
		self.CACHE_SONGS_PATH = "data/cache/songs.pkl"
		self.CACHE_SORTED_SONGS_PATH = "data/cache/sorted_songs.pkl"
		self.CONCLUSION_FILEPATH = "data/conclusions/"
		self.sorted_songs = dict()
		# Songs sorted by playlist and folders
		self.songs = list()

		self.get_playlists()

		if self.use_cache:
			self.recover_songs()

		self.sp = spotipy.Spotify(auth=self.token)

	def get_playlists(self):
		"""
		Gets playlists dict from saved file.
		"""
		with open(self.PLAYLIST_FILEPATH, "rb") as file:
			self.playlists = pickle.load(file)

	def walk_all(self):
		"""
		Walk method, applied to all playlists.
		"""
		if not len(self.songs):
			self.sorted_songs = self.walk_playlists(self.playlists)
			self.cache_songs()

	def walk_playlists(self, playlists):
		"""
		Methods that walks through folders and playlists
		"""
		sorted_playlists = dict()

		for playlist_name in playlists.keys():
			playlist = playlists[playlist_name]
			if type(playlist) is dict:
				# Folder
				print("Folder:", playlist_name)
				sorted_playlists[playlist_name] = self.walk_playlists(playlist)
			else:
				print("-", playlist_name)
				sorted_playlists[playlist_name] = self.add_songs_to_collection(playlist_name, playlist)

		return sorted_playlists

	def add_songs_to_collection(self, playlist_name, playlist):
		"""
		Methods that collect songs in sorted and individual lists.
		"""
		songs_collection = list()

		playlist = self.sp.playlist(playlist)
		tracks = playlist["tracks"]
		for song in tracks["items"]:
			song = song["track"]

			new_artists = list()
			for artist in song["artists"]:
				new_artists.append(artist["name"])
			# Generate a new artists list with only names

			new_song = {
				"name": song["name"],
				"album": song["album"]["name"],
				"artists": new_artists,
				"duration_ms": song["duration_ms"],
				"playlist": playlist_name,
				"id": song["id"],
			}
			# Only saves useful information
			songs_collection.append(new_song)

			# Looking for the same song in list
			for aux_song in self.songs:
				if new_song["id"] == aux_song["id"]:
					break
			else:
				self.songs.append(new_song)
			# Saves song with its properties

		return songs_collection

	def walk_each_song_through_folders(self):
		"""
		Takes songs from main lists, and passes them.
		"""
		out_songs = list()

		for playlist_name in self.sorted_songs.keys():
			playlist = self.sorted_songs[playlist_name]
			if type(playlist) is dict:
				# Folder
				pass
			else:
				for song in playlist:
					returned_song = self.search_song_in_folders(song)
					if returned_song:
						out_songs.append(returned_song)

		return out_songs

	def search_song_in_folders(self, song):
		"""
		Method that takes a song in one of the main playlists,
		and search it through folders. This is done due to my
		own method of songs organization.
		"""
		for playlist_name in self.sorted_songs.keys():
			playlist = self.sorted_songs[playlist_name]
			if type(playlist) is dict:
				folder = playlist
				for playlist in folder.keys():
					tracks = folder[playlist]
					for this_song in tracks:
						if this_song['id'] == song['id']:
							return None
			else:
				break
				# After folders there are main playlists, so I break

		# If song was not in any of the folders
		return song

	def search_artists_in_folders(self):
		"""
		Method that searches an artists in folders playlists that
		has its own artists folder.
		"""
		own_artists_list = [genre.lower() for genre in self.playlists["Artists"].keys()]

		folder = self.sorted_songs["Genres"]

		songs = list()

		for playlist in folder.keys():
			tracks = folder[playlist]
			for this_song in tracks:
				artists = this_song['artists']
				for artist in artists:
					if artist.lower() in own_artists_list:
						songs.append(this_song)

		return songs
						

	def walk_each_song_through_main_playlists(self):
		"""
		Takes songs from main folders, and passes them.
		"""
		out_songs = list()

		for playlist_name in self.sorted_songs.keys():
			playlist = self.sorted_songs[playlist_name]
			if type(playlist) is dict:
				folder = playlist
				for playlist in folder.keys():
					tracks = folder[playlist]
					for this_song in tracks:
						returned_song = self.search_song_in_main_playlists(this_song)
						if returned_song:
							out_songs.append(returned_song)
			else:
				break

		return out_songs

	def search_song_in_main_playlists(self, song):
		"""
		Method that takes a song in one of the folders,
		and search it through main playlists. This is done due to my
		own method of songs organization.
		"""
		for playlist_name in self.sorted_songs.keys():
			playlist = self.sorted_songs[playlist_name]
			if type(playlist) is dict:
				# Folder
				pass
			else:
				for this_song in playlist:
					if this_song['id'] == song['id']:
						return None

		return song

	def format_song(self, song):
		"""
		Formats a string of a song information as a easy way to read it,
		and returns string to print or save.
		"""
		artist_string = ""
		artists = song["artists"]
		if len(artists) == 1:
			artist_string = artists[0]
		elif len(artists) == 2:
			artist_string = f"{artists[0]} y {artists[1]}"
		else:
			for artist_index in range(len(artists) - 1):
				artist_string += artists[artist_index] + ", "

			artist_string += "y " + artists[-1]

		string = f"'{song['name']}' - {artist_string} - {song['playlist']}"

		return string

	def search_same_song(self):
		"""
		Methods that compares name and duration, to
		verify that is not the same song with different ID.
		"""
		repeated_songs = list()

		for song in self.songs:
			for another_song in self.songs:
				if song["name"] == another_song["name"]:
					if song["duration_ms"] == another_song["duration_ms"]:
						if song["id"] != another_song["id"]:
							# Different song, same attributes
							repeated_songs.append(song)
							break

		return repeated_songs

	def get_song_id(self, song_name):
		"""
		Receives a song name and returns its ID.
		"""
		for song in self.songs:
			if song["name"] == song_name:
				return song["id"]

		return None

	def get_all_song_appearances(self, song_id):
		"""
		Receives a song id and returns its apperances in
		any playlist.
		"""
		song_appearances = list()

		for playlist_name in self.sorted_songs.keys():
			playlist = self.sorted_songs[playlist_name]
			if type(playlist) is dict:
				# Folder
				folder = playlist
				for playlist in folder.keys():
					tracks = folder[playlist]
					for this_song in tracks:
						if this_song["id"] == song_id:
							song_appearances.append(this_song)
			else:
				for this_song in playlist:
					if this_song['id'] == song_id:
						song_appearances.append(this_song)

		return song_appearances

	def mix_playlist(self, playlist_name):
		"""
		Spotify random player sometimes is not effective. This method mix songs, in
		a better random critheria, and saves new playlist order.
		"""
		playlist = self.sorted_songs[playlist_name]
		new_playlist = list()

		for item in range(len(playlist)):
			if len(new_playlist) == 0:
				index = random.randint(0, len(playlist) - 1)
				new_playlist.append(playlist[index])
				playlist.pop(index)
				# Add first song because have nothing to compare
			else:
				for i in range(5):
					# Five attempts to get the best song for this place
					index = random.randint(0, len(playlist) - 1)

					for artist in playlist[index]["artists"]:
						if artist in new_playlist[-1]["artists"]:
							# Duplicated artists, skip
							break
					else:
						# Not duplicated artists
						new_playlist.append(playlist[index])
						playlist.pop(index)
						break

					continue # Duplicated artists, next
				else:
					# If there was not "ideal" song, I add the last one
					new_playlist.append(playlist[index])
					playlist.pop(index)

		return new_playlist

	def cache_songs(self):
		"""
		Generates a cache of got songs.
		"""
		with open(self.CACHE_SONGS_PATH, "wb") as file:
			pickle.dump(self.songs, file)

		with open(self.CACHE_SORTED_SONGS_PATH, "wb") as file:
			pickle.dump(self.sorted_songs, file)

	def recover_songs(self):
		"""
		Generates songs list from cache.
		"""
		with open(self.CACHE_SONGS_PATH, "rb") as file:
			self.songs = pickle.load(file)

		with open(self.CACHE_SORTED_SONGS_PATH, "rb") as file:
			self.sorted_songs = pickle.load(file)
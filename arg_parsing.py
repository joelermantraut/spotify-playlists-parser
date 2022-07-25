"""
Class to parse command line arguments and run spotify parser
class methods.
"""

import argparse

from printing import Printer
from spotify_parser import parsePlaylists

class ArgParsing():
	"""
	Class to parse command line arguments.
	"""
	def __init__(self, token):
		self.token = token
		self.parser = argparse.ArgumentParser(description='Software that collects information about user playlists')
		self.spoti_parser = None
		self.add_args()
		self.parse_args()

	def add_args(self):
		self.parser.add_argument("-c", "--cache", action="store_true", help="Use cached songs database")
		self.parser.add_argument("-s", "--scan", action="store_true", help="Scan all information and saves it")
		self.parser.add_argument("-g", "--get-song", help="Show information of a song by name")
		self.parser.add_argument("-m", "--mix-playlist", help="Mix playlist songs and saves results")
		self.parser.add_argument("-i", "--show-info", help="Show song info")
		self.parser.add_argument("--print-all", action="store_true", help="Print list of songs")

	def parse_args(self):
		args = self.parser.parse_args()

		if args.cache:
			cache = True
		else:
			cache = False

		self.spoti_parser = parsePlaylists(self.token, use_cache=cache)
		self.spoti_parser.walk_all()

		if args.scan:
			self.run_scan()

		if args.print_all:
			self.print_all()

		if args.get_song:
			self.get_song(args.get_song)

		if args.mix_playlist:
			self.mix_playlist(args.mix_playlist)

		if args.show_info:
			self.show_info(args.show_info)

	def run_scan(self):
		self.presentation("Total songs: " + str(len(self.spoti_parser.songs)))
		self.save_on_file("Songs Lists", self.spoti_parser, self.spoti_parser.songs)

		songs = self.spoti_parser.walk_each_song_through_folders()
		self.presentation("Songs not in folders: " + str(len(songs)))
		if len(songs) > 0:
			self.save_on_file("Songs not in folders", self.spoti_parser, songs)

		songs = self.spoti_parser.walk_each_song_through_main_playlists()
		self.presentation("Songs not in main playlists: " + str(len(songs)))
		if len(songs) > 0:
			self.save_on_file("Songs not in main playlists", self.spoti_parser, songs)

		songs = self.spoti_parser.search_same_song()
		self.presentation("Songs repeated: " + str(len(songs)))
		if len(songs) > 0:
			self.save_on_file("Songs Repeated", self.spoti_parser, songs)

	def get_song(self, song):
		ID = self.spoti_parser.get_song_id(song)
		if ID:
			song_appearances = self.spoti_parser.get_all_song_appearances(ID)

			self.presentation("Song Appearances")

			for song in song_appearances:
				print(self.spoti_parser.format_song(song))
		else:
			self.presentation("Song not found")

	def mix_playlist(self, playlist_name):
		new_playlist = self.spoti_parser.mix_playlist(playlist_name)

		self.save_on_file("New order - " + playlist_name, self.spoti_parser, new_playlist)

	def show_info(self, song_name):
		for song in self.spoti_parser.songs:
			if song["name"] == song_name:
				print("Name:", song["name"])
				print("Album:", song["album"])
				print("Artist/s: ", ", ".join(song["artists"]))
				print(
					"Duration:", 
					str(song["duration_ms"] // 60000), 
					"Minutos,", 
					str(round((song["duration_ms"] / 60000 - song["duration_ms"] // 60000) * 60)), 
					"segundos."
				)
				print(
					"Playlist/s:",
					", ".join([song["playlist"]
						for song in self.spoti_parser.get_all_song_appearances(
							self.spoti_parser.get_song_id(song_name))]
						)
				)
				print("ID:", song["id"])

	def print_all(self):
		if len(self.spoti_parser.songs):
			print(spoti_parser.songs)

	def presentation(self, string):
		"""
		Function to print a title before each section.
		"""
		Printer().color_print(string, "grey", "green")

	def save_on_file(self, title, parser, songs):
		"""
		Saves lists of songs in a file.
		"""
		with open(self.spoti_parser.CONCLUSION_FILEPATH + title + ".txt", "w", encoding="utf-8") as file:
			for song in songs:
				string_formatted = parser.format_song(song)
				file.write(string_formatted + "\n")
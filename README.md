# Spotify Playlists Parser

# Introduction
This is an app that connects to a user Spotify library, and reads it to bring information and conclusions about it.
Specifically, it responds to my way of music organization, where I have two folders called "Artists" and "Genres". In them I save, sorted, all the music
I like or liked. Then, there are any numbers of playlists (main playlists), where I mix all my music, in the way I prefer it.

So, its interesting for me to be sure that all songs in main playlists are in their respective folder. Otherwise, if I decide to delete a playlists, I would
lose some of the not saved songs.
In the same way, I would want to know how many of the music in folders, are used in main playlists.
When running scan test, all this information in printed in terminal. Also, some functions were added to main script.

# Usage
Run following command to get usage help:

`python main.py -h`

```
usage: main.py [-h] [-c] [-s] [--print-all] [-g GET_SONG]

Software that collects information about user playlists

optional arguments:
  -h, --help            show this help message and exit
  -c, --cache           Use cached songs database
  -s, --scan            Scan all information and saves it
  --print-all           Print list of songs
  -g GET_SONG, --get-song GET_SONG
                        Show information of a song by name
```

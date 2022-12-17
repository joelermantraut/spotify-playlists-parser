# Spotify Playlists Parser

# Introduction
This is an app that connects to a user Spotify library, and reads it to bring information and conclusions about it.

Specifically, it responds to my way of music organization, where I have two folders called "Artists" and "Genres". In them I save, sorted, all the music
I like or liked. Then, there are any numbers of playlists (main playlists), where I mix all my music, in the way I prefer it.

So, its interesting for me to be sure that all songs in main playlists are in their respective folder. Otherwise, if I decide to delete a playlists, I would
lose some of the not saved songs. In the same way, I would want to know how many of the music in folders, are used in main playlists.
When running scan test, all this information is printed in terminal.

Also, some functions were added to main script, for example to search a song appearances.

# Setting Up
1. First, install dependencies with requeriments.txt file:
`pip install -r requirements.txt`
2. After it, create a data folder, inside root folder.
3. In "generation_scripts" folder, there are two script. Edit "credentials_file.py" to generate .credentials file:
`python -m credentials_file.py`
4. Then, edit "playlists_dict_generator.py", adding your playlists. Run it from root folder, and a playlists.pkl file will be generated in data folder: `python -m generation_scripts/playlists_dict_generator.py`

`NOTE:` Run them from generation_scripts folder, otherwise it will not work.

# Usage
Run following command to get usage help:

`python main.py -h`

```
usage: main.py [-h] [-c] [-s] [-g GET_SONG] [-m MIX_PLAYLIST] [-i SHOW_INFO] [--print-all]

Software that collects information about user playlists

optional arguments:
  -h, --help            show this help message and exit
  -c, --cache           Use cached songs database
  -s, --scan            Scan all information and saves it
  -g GET_SONG, --get-song GET_SONG
                        Show information of a song by name
  -m MIX_PLAYLIST, --mix-playlist MIX_PLAYLIST
                        Mix playlist songs and saves results
  -i SHOW_INFO, --show-info SHOW_INFO
                        Show song info
  --print-all           Print list of songs
```

# Disclaimer
Don't forget that this was done thinking in my organization method, explained before. If it you don't use it, it would work, as it would not.

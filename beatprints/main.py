"""
Serves as the main entry point for the BeatPrints application. 
Orchestrates the process of generating posters for songs, including 
fetching song information, processing images, and generating posters.

Dependencies:
    - PIL: Image processing.
    - pathlib: Filesystem paths.
    - tabulate: Printing tables.
    - image: Image processing functions.
    - lyrics: Retrieving and processing song lyrics.
    - spotify: Interacting with Spotify API.
    - utils: Utility functions.
    - rich: Pretty-printing texts.

Usage:
    Run this module to generate posters for songs based on user input.
"""

import os
import dotenv
import tabulate

from rich import print
from lyrics import Lyrics
from poster import Poster
from spotify import Spotify

import utils

dotenv.load_dotenv()

# Retrieving Spotify API from environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Intialize classes
ly = Lyrics()
sp = Spotify(CLIENT_ID, CLIENT_SECRET)
ps = Poster(save_path="../images/")

# Get input for Image and Accent
IMAGE = utils.validate_image_path() if utils.c_input(
    "🌃 • Do you want to include a custom image as the cover of the poster?"
) else None

ACCENT = utils.c_input(
    "🤌 • Would you like to add a stylish color accent at the bottom of your poster?"
)

# Search for Tracks
track_search = input("🎺 • Search for your favourite song: ")

# Pretty print lists
tracks = sp.search_track(track_search)
header = ["*", "Name", "Artist", "Album"]

table = utils.remove_column(tracks, 4)
print(tabulate.tabulate(table, header, "rounded_outline"))

# Get choices
choice = int(input("📋️ • Select your song right here: "))
track_selected = tracks[choice - 1]

# Get trackinfo and lyrics
track_info = sp.trackinfo(track_selected)

# Extract the lyrics based on the selection
lyrics = ly.get_lyrics(track_selected[1].split(' - ')[0], track_selected[2])
extracted = utils.get_extract(lyrics)

# Generate Poster
ps.generate(track_info, extracted, ACCENT, IMAGE)

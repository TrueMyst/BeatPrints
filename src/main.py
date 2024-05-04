"""
Module: main.py

This module serves as the main entry point for the BeatPrints application. 
It orchestrates the process of generating posters for songs, 
including fetching song information, processing images, and generating posters.

Dependencies:
    - pathlib: For working with filesystem paths.
    - PIL: Python Imaging Library for image processing tasks.
    - image: Custom module for image processing functions.
    - lyrics: Custom module for retrieving and processing song lyrics.
    - spotify: Custom module for interacting with the Spotify API.
    - utils: Custom module containing utility functions.
    - rich: Pretty-print texts.

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

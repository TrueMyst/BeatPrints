"""
Module: __main__.py

This module serves as the main entry point for the BeatPrints application.
It orchestrates the process of generating posters for songs,
including fetching song information, processing images, and generating posters.

Dependencies:
    - os: Provides a way to interact with the operating system.
    - dotenv: Loads environment variables from a .env file.
    - tabulate: Pretty-prints tabular data in a visually appealing format.
    - rich: Provides rich text and beautiful formatting in the terminal.
    - lyrics: Custom module for retrieving and processing song lyrics.
    - poster: Custom module for generating posters.
    - spotify: Custom module for interacting with the Spotify API.
    - utils: Custom module containing utility functions.

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

from utils import select_lines, remove_column, confirm_input, validate_image_path

def main():
    dotenv.load_dotenv()

    # Retrieving Spotify API & MXM API credentials from environment variables
    MXM_TOKEN = os.getenv("MXM_USERTOKEN")
    LF_TOKEN = os.getenv("LF_USERTOKEN")
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    # Intialize classes
    ly = Lyrics(MXM_TOKEN, LF_TOKEN)
    sp = Spotify(CLIENT_ID, CLIENT_SECRET)
    ps = Poster(save_path="../images/")

    # Get input for Image and Accent
    IMAGE = validate_image_path() if confirm_input(
        "🌃 • Do you want to include a custom image as the cover of the poster?") else None

    ACCENT = confirm_input(
        "🤌 • Would you like to add a stylish color accent at the bottom of your poster?")

    # Search for Tracks
    track_search = input("🎺 • Search for your favourite song: ")

    # Pretty print lists
    tracks = sp.search_track(track_search)
    header = ["*", "Name", "Artist", "Album"]

    table = remove_column(tracks, 4)
    print(tabulate.tabulate(table, header, "rounded_outline"))

    # Get choices
    choice = int(input("📋️ • Select your song right here: "))
    track_selected = tracks[choice - 1]

    # Get trackinfo and lyrics
    track_info = sp.trackinfo(track_selected)
    lyrics = ly.get_lyrics(track_selected[1], track_selected[2])

    for line_num, line in enumerate(str(lyrics).split("\n")):
        print(f"[bold magenta]{line_num + 1:2}[/bold magenta] {line}")

    # Select lyrics
    selected = input("🍀. Select any 4 lines (eg. 7-10): ")
    lyrics = select_lines(str(lyrics), selected)

    # Generate Poster
    ps.generate(track_info, lyrics, ACCENT, IMAGE)

if __name__ == "__main__":
    main()
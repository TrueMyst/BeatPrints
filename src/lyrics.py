"""
Module: lyrics.py

This module provides functions for retrieving and processing song lyrics using the PyMusix library.

Dependencies:
    - os: Operating system interfaces (used for environment variables).
    - sys: System-specific parameters and functions (used for exiting the program).
    - rich: Rich text formatting for console output.
    - pymusix: Python wrapper for the MusixMatch API.
    - dotenv: Loads environment variables from a .env file.

Functions:
    - select_lines(lyrics, selection): Select specific lines from the lyrics based on the range.
    - get_extract(name, artist): Search for a song and retrieve a portion of its lyrics.

Usage:
    To use this module, ensure that you have the necessary environment variables set up:
    - SPOTIFY_CLIENT_ID: Spotify client ID for accessing the MusixMatch API.
    - SPOTIFY_CLIENT_SECRET: Spotify client secret for accessing the MusixMatch API.
    - MUSIXMATCH_USERTOKEN: User token for accessing the MusixMatch API.
"""

import os
import sys

from rich import print
from pymusix import PyMusix
from dotenv import load_dotenv

try:
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve Spotify and MusixMatch API credentials from environment variables
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    USER_TOKEN = os.getenv("MUSIXMATCH_USERTOKEN")

    # Initialize PyMusix object with API credentials
    song = PyMusix()
    song.set_secrets(CLIENT_ID, CLIENT_SECRET, USER_TOKEN)

except FileNotFoundError:
    print("Error: .env file not found.")
    sys.exit(1)

except KeyError as e:
    print(f"Error: Environment variable {e} not found.")
    sys.exit(1)

except ValueError:
    print("Error: Invalid selection range.")
    sys.exit(1)

except IndexError:
    print("Error: Selection range out of bounds.")
    sys.exit(1)


def select_lines(lyrics: str, selection: str):
    """
    Selects specific lines from the lyrics based on the provided range.

    Args:
        lyrics (str): The full lyrics of the song.
        selection (str): The range of lines to select (e.g., "2-5, 7-10").

    Returns:
        str: The selected lines of lyrics.
    """

    lines = lyrics.strip().split("\n")
    line_count = len(lines)

    try:
        selected = [int(num) for num in selection.split("-")]
        if (
            len(selected) != 2
            or selected[0] >= selected[1]
            or selected[0] <= 0
            or selected[1] > line_count
        ):
            return "Invalid selection. Please provide a valid range within the line numbers."

        selected_lines = lines[selected[0] - 1 : selected[1]]
        return "\n".join(selected_lines)

    except ValueError:
        return (
            "Invalid input. Please provide a valid range using the format 'line x-y'."
        )


def get_extract(name: str, artist: str):
    """
    Searches for a song and retrieves a portion of its lyrics.

    Args:
        name (str): The name of the song.
        artist (str): The name of the artist.

    Returns:
        str: The extracted portion of the lyrics.
    """

    # Search and retrieve song lyrics
    try:
        song.search_track(name, artist)
        lyrics = str(song.lyrics)

        print("\n[💫] Retrieved lyrics successfully\n")

        # Print the lyrics for user selection
        for line_num, line in enumerate(lyrics.split("\n")):
            print(f"[bold magenta]{line_num + 1:2}[/bold magenta] {line}")

        # Prompt the user to select favorite lines
        while True:
            lines = input(
                "\n[🎺] You may ignore the spaces between the lines of the song.\n"
                "[🍀] Select any 4 of your favorite lines from here "
                "(e.g., 2-5, 7-10): "
            )

            # Validate and return the selected lines
            result = select_lines(lyrics, lines)
            result = "\n".join(line for line in result.split("\n") if line.strip())

            if not result.startswith("Invalid"):
                selected_lines = result.split("\n")
                if 2 <= len(selected_lines) <= 4:
                    return result
                else:
                    print("Please select exactly 4 lines.")

    except Exception:
        print("\n[😓] Unfortunately, the lyrics were not found from MusixMatch.")
        print("[📝] You can paste the lyrics manually below:")

        # Allow user to input lyrics manually
        manual_lyrics = []
        for _ in range(4):
            line = input()
            manual_lyrics.append(line)

        return "\n".join(manual_lyrics)

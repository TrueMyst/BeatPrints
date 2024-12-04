"""
Module: utils.py

Provides utility functions for Spotify and Lyrics operations.
"""

import re
import random
import string
import datetime

from . import write
from . import consts


def organize_tracks(tracks: list) -> tuple:
    """
    Organizes tracks into columns that fit within the maximum width.

    Args:
        draw (ImageDraw.ImageDraw): Draw context for calculating text widths.
        tracks (list): List of track names.

    Returns:
        tuple: Organized tracks into columns and their respective widths.
    """
    while True:
        # Split tracks into columns of MAX_ROWS each
        columns = [
            tracks[i : i + consts.MAX_ROWS]
            for i in range(0, len(tracks), consts.MAX_ROWS)
        ]

        # Calculate the width of the longest track in each column
        max_tracks = [max(col, key=len) for col in columns]
        track_widths = [
            write.get_length(track, write.font("Light"), consts.S_TRACKS)
            for track in max_tracks
        ]

        # Calculate total width and check if it fits within the allowed space
        total_width = sum(track_widths) + consts.S_SPACING * (len(columns) - 1)
        if total_width <= consts.MAX_WIDTH:
            break  # Fits, so exit the loop
        else:
            # Remove the longest track from the longest column and retry
            longest_column_index = track_widths.index(max(track_widths))
            longest_column = columns[longest_column_index]
            tracks.remove(max(longest_column, key=len))

    return columns, track_widths


def special_code() -> int:
    """
    Generates a special code based on the current timestamp.

    Returns:
        int: The generated special code.
    """
    return ((int(datetime.datetime.now().timestamp()) % 100000) + 100000) % 100000


def create_filename(song: str, artist: str) -> str:
    """
    Creates a safe filename based on the song and artist names.

    Args:
        song (str): The name of the song.
        artist (str): The name of the artist.

    Returns:
        str: The safe filename.
    """
    full_text = f"{song} by {artist}"

    # Replace illegal characters with underscores and sanitize
    safe_text = (
        re.sub(r'[<>:"/\\|?*\x00-\x1F\x7F]', "_", full_text)
        .strip()
        .strip(".")
        .lower()
        .replace(" ", "_")
    )

    # Remove consecutive underscores
    safe_text = re.sub(r"_{2,}", "_", safe_text)

    # Limit filename length to 255 characters
    safe_text = safe_text[:255]

    # Append 3 random hexadecimal digits
    random_hex = "".join(random.choices(string.hexdigits[:-6], k=3))
    filename = f"{safe_text}_{random_hex}.png"

    return filename

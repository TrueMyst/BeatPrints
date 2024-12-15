"""
Module: utils.py

Provides utility functions for Spotify and Lyrics operations.
"""

import re
import random
import string

from . import write, consts


def organize_tracks(tracks: list) -> tuple:
    """
    Organizes tracks into columns that fit within the maximum allowed width.

    Args:
        tracks (list): List of track names to be organized.

    Returns:
        tuple: A tuple containing two elements:
            - List of lists where each inner list contains a column of track names.
            - List of widths for each track column.
    """
    while True:
        # Split tracks into columns with a maximum of MAX_ROWS per column
        columns = [
            tracks[i : i + consts.MAX_ROWS]
            for i in range(0, len(tracks), consts.MAX_ROWS)
        ]

        # Determine the width of the longest track in each column
        max_tracks = [max(col, key=len) for col in columns]
        track_widths = [
            write.calculate_text_width(track, write.font("Light"), consts.S_TRACKS)
            for track in max_tracks
        ]

        # Sum the total width and check if it fits within the allowed MAX_WIDTH
        total_width = sum(track_widths) + consts.S_SPACING * (len(columns) - 1)

        if total_width <= consts.MAX_WIDTH:
            break  # If it fits, exit the loop

        else:
            # If it doesn't fit, remove the longest track from the longest column
            longest_column_index = track_widths.index(max(track_widths))
            longest_column = columns[longest_column_index]
            tracks.remove(max(longest_column, key=len))

    return columns, track_widths


def filename(song: str, artist: str) -> str:
    """
    Creates a safe filename based on the song and artist names.

    Args:
        song (str): The name of the song.
        artist (str): The name of the artist.

    Returns:
        str: A sanitized filename that is safe for file systems.
    """
    full_text = f"{song} by {artist}"

    # Replace illegal characters (e.g., "<", ":", "/") with underscores and sanitize the text
    safe_text = (
        re.sub(r'[<>:"/\\|?*\x00-\x1F\x7F]', "_", full_text)
        .strip()
        .strip(".")
        .lower()
        .replace(" ", "_")
    )

    # Remove consecutive underscores
    safe_text = re.sub(r"_{2,}", "_", safe_text)

    # Limit filename length to 255 characters (filesystem limit)
    safe_text = safe_text[:255]

    # Append 3 random hexadecimal digits to make the filename unique
    random_hex = "".join(random.choices(string.hexdigits[:-6], k=3))
    filename = f"{safe_text}_{random_hex}.png"

    return filename

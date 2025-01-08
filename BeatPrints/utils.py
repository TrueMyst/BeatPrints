"""
Module: utils.py

Provides utility functions for Spotify and Lyrics operations.
"""

import re
import random
import string

from . import write, consts


def add_flat_indexes(nlist: list) -> list:
    """
    Adds a flat index to each track name in a nested list.

    Args:
        nlist (list): A nested list of track names.

    Returns:
        list: The modified nested list with flat indexes added to track names.
    """

    index = 1

    for idx, cols in enumerate(nlist):
        for jdx, row in enumerate(cols):

            nlist[idx][jdx] = f"{index}. {row}"
            index += 1

    return nlist


def organize_tracks(tracks: list, indexing: bool = False) -> tuple:
    """
    Organizes tracks into columns that fit within the maximum allowed width.

    Args:
        tracks (list): List of track names to be organized.

    Returns:
        tuple: A tuple containing two elements:
            - List of lists where each inner list contains a column of track names.
            - List of widths for each track column.
    """

    def calculate_column_width(tracks_column: list, additional_width: int = 0):
        """
        Helper function to calculate the width of the longest track in a column.
        """

        tracks = max(tracks_column, key=len)

        return (
            write.calculate_text_width(tracks, write.font("Light"), consts.S_TRACKS)
            + additional_width
        )

    additional_width = 0

    # Account for the space that index numbers take
    if indexing:
        index = len(tracks) + 1

        additional_width = write.calculate_text_width(
            f"{index}", write.font("Light"), consts.S_TRACKS
        )

    while True:
        # Split tracks into columns with a maximum of MAX_ROWS per column
        columns = [
            tracks[i : i + consts.MAX_ROWS]
            for i in range(0, len(tracks), consts.MAX_ROWS)
        ]

        # Determine the width of each column
        track_widths = [
            calculate_column_width(col, additional_width) for col in columns
        ]

        # Sum the total width and check if it fits within the allowed MAX_WIDTH
        total_width = sum(track_widths) + consts.S_SPACING * (len(columns) - 1)

        if total_width <= consts.MAX_WIDTH:
            break  # If it fits, exit the loop

        else:
            # If it doesn't fit, remove the longest track from the column with the widest width
            longest_column_index = track_widths.index(max(track_widths))
            longest_column = columns[longest_column_index]
            tracks.remove(max(longest_column, key=len))

    # Add flat indexes to tracks if indexing is enabled
    if indexing:
        columns = add_flat_indexes(columns)

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

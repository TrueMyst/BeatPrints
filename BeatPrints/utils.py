"""
Module: utils.py

Provides utility functions for Spotify and Lyrics operations.
"""

import re
import random
import string

from BeatPrints import write
from BeatPrints.consts import Size, Position

# Initialize the components
s = Size()
p = Position()


def add_indexes(nlist: list) -> list:
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


def organize_tracks(tracks: list, index: bool = False) -> tuple:
    """
    Distributes tracks into columns while ensuring they fit within the maximum allowed width.

    Parameters:
        tracks (list): A list of track names to be organized into columns.
        index (bool, optional): If True, adds index numbers to the tracks. Defaults to False.

    Returns:
        tuple: A tuple containing:
            - list: The organized columns of tracks.
            - list: The width of each column.
    """

    def get_column_width(cols: list, idx_width: int) -> int:
        """
        Calculates the width of a column, accounting for index spacing if applicable.
        """

        size = s.TRACKS
        font = write.font("Light")

        return max(write.text_width(item, font, size) for item in cols) + idx_width

    # Determine index width if index is True
    idx_width = write.text_width("00. ", write.font("Light"), s.TRACKS) if index else 0

    while True:
        # Split tracks into columns based on MAX_ROWS
        cols = [tracks[i : i + s.MAX_ROWS] for i in range(0, len(tracks), s.MAX_ROWS)]

        # Compute widths of each column
        col_widths = [get_column_width(col, idx_width) for col in cols]

        # Calculate total width including spacing
        total_width = sum(col_widths) + s.SPACING * (len(cols) - 1)

        if total_width <= s.MAX_WIDTH:
            # If columns fit within the max width, stop adjusting
            break

        # Otherwise, remove the longest track from the widest column
        widest_col = cols[col_widths.index(max(col_widths))]
        tracks.remove(max(widest_col, key=len))

    # Add indexes to tracks if enabled
    if index:
        cols = add_indexes(cols)

    return cols, col_widths


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

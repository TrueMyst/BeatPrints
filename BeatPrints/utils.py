"""
Module: utils.py

Provides various utility functions for Spotify and Lyrics operations.

Imports:
    - re: Regular expression operations.
    - random: Generate random values.
    - string: String manipulation utilities.
    - datetime: Date and time handling.
"""

import re
import random
import string
import datetime


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

"""
Module: lyrics.py

Provides functionality for retrieving song lyrics using the LRClib API.
"""

import re
from lrclib import LrcLibAPI

from .spotify import TrackMetadata
from .errors import (
    NoLyricsAvailable,
    InvalidFormatError,
    InvalidSelectionError,
    LineLimitExceededError,
)


class Lyrics:
    """
    A class for interacting with the LRClib API to fetch and manage song lyrics.
    """

    def get_lyrics(self, metadata: TrackMetadata) -> str:
        """
        Retrieves lyrics from LRClib.net for a specified track and artist.

        Args:
            metadata (TrackMetadata): An object containing the track's metadata.

        Returns:
            str: The lyrics in plain text, if available.

        Raises:
            NoLyricsAvailable: If no lyrics are found for the specified track and artist.
        """
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
        )

        # Prepare the LRClib API with the user agent
        api = LrcLibAPI(user_agent=user_agent)
        id = api.search_lyrics(track_name=metadata.name, artist_name=metadata.artist)

        # Check if lyrics are available
        if len(id) != 0:
            lyrics = api.get_lyrics_by_id(id[0].id).plain_lyrics
            return str(lyrics)
        else:
            raise NoLyricsAvailable

    def select_lines(self, lyrics: str, selection: str) -> str:
        """
        Extracts a specific range of lines from the given song lyrics.

        Args:
            lyrics (str): The full lyrics of the song as a single string.
            selection (str): The range of lines to extract, specified in the format "start-end" (e.g., "2-5").

        Returns:
            str: The extracted lines, exactly 4 in total, as a single string.

        Raises:
            InvalidFormatError: If the selection argument is not in the correct "start-end" format.
            InvalidSelectionError: If the specified range is out of bounds or otherwise invalid.
            LineLimitExceededError: If the selected range does not include exactly 4 lines.
        """

        # Split lyrics into lines
        lines = [line for line in lyrics.split("\n")]
        line_count = len(lines)

        try:
            pattern = r"^\d+-\d+$"

            # Check if selection matches the "start-end" format
            if not re.match(pattern, selection):
                raise InvalidFormatError

            selected = [int(num) for num in selection.split("-")]

            # Validate the selection range
            if (
                len(selected) != 2
                or selected[0] >= selected[1]
                or selected[0] <= 0
                or selected[1] > line_count
            ):
                raise InvalidSelectionError

            # Extract the selected lines and remove empty lines
            extracted = lines[selected[0] - 1 : selected[1]]
            selected_lines = [line for line in extracted if line != ""]

            # Ensure exactly 4 lines are selected
            if len(selected_lines) != 4:
                raise LineLimitExceededError

            quatrain = "\n".join(selected_lines).strip()
            return quatrain

        except Exception as e:
            raise e

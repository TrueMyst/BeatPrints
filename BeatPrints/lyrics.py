"""
Module: lyrics.py

Provide lyrics from LRClib API.
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
    This class helps to retrieve lyrics through LRClib API.
    """

    def get_lyrics(self, metadata: TrackMetadata) -> str:
        """
        Retrieve lyrics from LRClib.net for a given track and artist.

        Args:
            metadata (TrackMetadata): Instance that holds the metadata about a track.

        Returns:
            str: The lyrics in plain text if found.

        Raises:
            NoLyricsAvailable: If no lyrics are found for the given track and artist.
        """

        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
        )

        # Prepare the API
        api = LrcLibAPI(user_agent=user_agent)
        id = api.search_lyrics(track_name=metadata.name, artist_name=metadata.artist)

        # Check if lyrics are available
        if len(id) != 0:
            lyrics = api.get_lyrics_by_id(id[0].id)
            return str(lyrics.plain_lyrics)
        else:
            raise NoLyricsAvailable

    def select_lines(self, lyrics: str, selection: str) -> str:
        """
        Selects a specific range of lines from the provided lyrics.

        Args:
            lyrics (str): The full lyrics of the song.
            selection (str): The selection range in the format "start-end".

        Returns:
            str: The selected lines of lyrics.

        Raises:
            InvalidFormatError: If the selection format is invalid.
            InvalidSelectionError: If the selection range is invalid.
            LineLimitExceededError: If the selected range doesn't contain exactly 4 lines.
        """
        lines = [line for line in lyrics.split("\n")]
        line_count = len(lines)

        try:
            pattern = r"^\d+-\d+$"

            if not re.match(pattern, selection):
                raise InvalidFormatError

            selected = [int(num) for num in selection.split("-")]

            if (
                len(selected) != 2
                or selected[0] >= selected[1]
                or selected[0] <= 0
                or selected[1] > line_count
            ):
                raise InvalidSelectionError

            portion = lines[selected[0] - 1 : selected[1]]
            selected_lines = [line for line in portion if line != ""]

            if len(selected_lines) != 4:
                raise LineLimitExceededError

            result = "\n".join(selected_lines).strip()
            return result

        except Exception as e:
            raise e

"""
Module: lyrics.py

Provide lyrics from LRClib API.

Imports:
    - re: Regex operations.
    - errors: For errors handling.
    - lrclib: Retrieving lyrics from LRClib.
"""

import re
import errors

from lrclib import LrcLibAPI


class Lyrics:
    """
    This class helps to retrieve lyrics through LRClib API.
    """

    def get_lyrics(self, name: str, artist: str) -> str:
        """
        Retrieve lyrics from LRClib.net for a given track and artist.

        Args:
            name (str): The name of the track.
            artist (str): The artist of the track.

        Returns:
            str: The lyrics in plain text if found.

        Raises:
            errors.NoLyricsAvailable: If no lyrics are found for the given track and artist.
        """

        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
        )

        # Prepare the API
        api = LrcLibAPI(user_agent=user_agent)
        id = api.search_lyrics(track_name=name, artist_name=artist)

        # Check if lyrics are available
        if len(id) != 0:
            lyrics = api.get_lyrics_by_id(id[0].id)
            return str(lyrics.plain_lyrics)
        else:
            raise errors.NoLyricsAvailable

    def select_lines(self, lyrics: str, selection: str) -> str:
        """
        Selects a specific range of lines from the provided lyrics.

        Args:
            lyrics (str): The full lyrics of the song.
            selection (str): The selection range in the format "start-end".

        Returns:
            str: The selected lines of lyrics.

        Raises:
            errors.InvalidFormatError: If the selection format is invalid.
            errors.InvalidSelectionError: If the selection range is invalid.
            errors.LineLimitExceededError: If the selected range doesn't contain exactly 4 lines.
        """
        lines = [line for line in lyrics.split("\n")]
        line_count = len(lines)

        try:
            pattern = r"^\d+-\d+$"

            if not re.match(pattern, selection):
                raise errors.InvalidFormatError

            selected = [int(num) for num in selection.split("-")]

            if (
                len(selected) != 2
                or selected[0] >= selected[1]
                or selected[0] <= 0
                or selected[1] > line_count
            ):
                raise errors.InvalidSelectionError

            portion = lines[selected[0] - 1 : selected[1]]
            selected_lines = [line for line in portion if line != ""]

            if len(selected_lines) != 4:
                raise errors.LineLimitExceededError

            result = "\n".join(selected_lines).strip()
            return result

        except Exception as e:
            raise e

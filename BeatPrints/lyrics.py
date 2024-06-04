"""
Module: lyrics.py

Retrieve lyrics through LRC API

Imports:
    - errors: For handling errors.
    - lrclib: Retrieving lyrics from LRClib.

"""

import errors
from lrclib import LrcLibAPI


class Lyrics:
    """
    This class helps to retrieve lyrics with the help of LRC API.
    """

    def __init__(self):
        pass

    def get_lyrics(self, name: str, artist: str):
        """
        Retrieve lyrics from LRClib.net.

        Args:
            name (str): Track's name.
            artist (str): Track's artist.

        Returns:
            str or None: The lyrics in plain text if found, otherwise None.
        """

        user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"

        # Preparing the API
        api = LrcLibAPI(user_agent=user_agent)
        id = api.search_lyrics(track_name=name, artist_name=artist)

        # Check if lyrics are available
        if len(id) != 0:
            lyrics = api.get_lyrics_by_id(id[0].id)
            return lyrics.plain_lyrics

        else:
            return None

    def select_lines(self, lyrics: str, selection: str) -> str:
        """
        Selects specific lines from the lyrics based on the provided range.

        Args:
            lyrics (str): The full lyrics of the song.
            selection (str): The range of lines to select (e.g., "2-5, 7-10").

        Returns:
            str: The selected lines of lyrics.
        """

        # Remove empty lines from the lyrics
        lines = [line for line in lyrics.split("\n")]
        line_count = len(lines)

        try:
            selected = [int(num) for num in selection.split("-")]

            # Conditions to check whether the range is valid or not
            if (len(selected) != 2 or selected[0] >= selected[1]
                    or selected[0] <= 0 or selected[1] > line_count):
                raise errors.InvalidSelectionError

            # Selects the part of the lyrics
            portion = lines[selected[0] - 1:selected[1]]
            selected_lines = [line for line in portion if line != '']

            if len(selected_lines) > 4:
                raise errors.LineLimitExceededError

            # Returns the result
            result = "\n".join(selected_lines).strip()
            return result

        except ValueError:
            raise errors.InvalidInputError

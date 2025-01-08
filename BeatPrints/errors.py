"""
Module: errors.py

Handles custom exceptions for error handling.
"""


class NoMatchingTrackFound(Exception):
    """
    Raised when no song matching the specified query is found.
    """

    def __init__(self, message="No track was found matching the query."):
        self.message = message
        super().__init__(self.message)


class NoMatchingAlbumFound(Exception):
    """
    Raised when no album matching the specified query is found.
    """

    def __init__(self, message="No album was found matching the query."):
        self.message = message
        super().__init__(self.message)


class NoLyricsAvailable(Exception):
    """
    Raised when no lyrics are available for the specified song.
    """

    def __init__(self, message="No lyrics were found for the specified song"):
        self.message = message
        super().__init__(self.message)


class InvalidSearchLimit(Exception):
    """
    Raised when an invalid search limit is specified for tracks or albums.
    """

    def __init__(self, message="The search limit must be set to at least 1."):
        self.message = message
        super().__init__(self.message)


class InvalidSelectionError(Exception):
    """
    Raised when an invalid selection range is provided for lyrics.
    """

    def __init__(
        self,
        message="Invalid range format. Please use 'start-end', ensuring start is less than end.",
    ):
        self.message = message
        super().__init__(self.message)


class LineLimitExceededError(Exception):
    """
    Raised when the selection in lyrics contains more or fewer than 4 lines.
    """

    def __init__(self, message="Exactly 4 lines must be selected, no more, no less."):
        self.message = message
        super().__init__(self.message)


class InvalidFormatError(Exception):
    """
    Raised when the format of the lyrics selection is invalid.
    """

    def __init__(self, message="Use format 'x-y' where x and y are numbers."):
        self.message = message
        super().__init__(self.message)


class ThemeNotFoundError(Exception):
    """
    Raised when the specified theme is not found or is invalid.
    """

    def __init__(
        self,
        message="The specified theme could not be found. Please ensure the theme name is valid.",
    ):
        self.message = message
        super().__init__(self.message)

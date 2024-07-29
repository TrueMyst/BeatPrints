class NoMatchingSongFound(Exception):
    """
    Exception raised when no song matching the query is found.
    """

    def __init__(self, message="No song found matching the query."):
        self.message = message
        super().__init__(self.message)


class NoLyricsAvailable(Exception):
    """
    Exception raised when no lyrics are available for the song.
    """

    def __init__(self, message="No lyrics found for the song."):
        self.message = message
        super().__init__(self.message)


class InvalidTrackLimit(Exception):
    """
    Exception raised when an invalid track limit is set for a Spotify search.
    """

    def __init__(self, message="Track limit must be at least 1."):
        self.message = message
        super().__init__(self.message)


class InvalidSelectionError(Exception):
    """
    Exception raised for an invalid selection range in lyrics.
    """

    def __init__(
        self,
        message="Invalid range format. Please use 'start-end', ensuring start is less than end.",
    ):
        self.message = message
        super().__init__(self.message)


class LineLimitExceededError(Exception):
    """
    Exception raised when more or less than 4 lines are selected in lyrics.
    """

    def __init__(self, message="Exactly 4 lines must be selected, no more, no less."):
        self.message = message
        super().__init__(self.message)


class InvalidFormatError(Exception):
    """
    Exception raised when the selection format for lyrics is invalid.
    """

    def __init__(self, message="Use format 'x-y' where x and y are numbers."):
        self.message = message
        super().__init__(self.message)

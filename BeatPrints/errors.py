class InvalidSelectionError(Exception):
    """Exception raised for invalid line selection."""

    def __init__(
        self,
        message="❓️ • Invalid selection, please provide a valid range within the line numbers."
    ):
        self.message = message
        super().__init__(self.message)


class LineLimitExceededError(Exception):
    """Exception raised when the selected lines exceed the limit."""

    def __init__(self, message="😓 • You can exactly select up to 4 lines."):
        self.message = message
        super().__init__(self.message)


class InvalidInputError(Exception):
    """Exception raised for invalid input format."""

    def __init__(
        self,
        message="❓️ • Invalid input, please provide a valid range using the format 'line x-y'."
    ):
        self.message = message
        super().__init__(self.message)

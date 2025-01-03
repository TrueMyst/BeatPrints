import os

from PIL import Image
from pathlib import Path
from questionary import Validator, ValidationError


class NumericValidator(Validator):

    def __init__(self, limit):
        self.limit = limit

    def validate(self, document):
        num = document.text.isdigit()

        if not num:
            raise ValidationError(
                message="> Please enter a valid number (only digits allowed)."
            )

        if document.text.isdigit() and (
            int(document.text) < 1 or int(document.text) > self.limit
        ):
            raise ValidationError(
                message=f"> Please enter a valid number between 1 - {self.limit}."
            )


class ImagePathValidator(Validator):

    def validate(self, document):
        filepath = Path(document.text).expanduser().resolve()

        if not os.path.isfile(filepath):
            raise ValidationError(
                message="> The provided path does not exist or is not a file.",
                cursor_position=len(document.text),  # Move cursor to end
            )

        try:
            with Image.open(filepath) as img:
                img.verify()  # Verify if it's an image file

        except (IOError, SyntaxError):
            raise ValidationError(
                message="> The provided file is not a recognized image format.",
                cursor_position=len(document.text),  # Move cursor to end
            )


class SelectionValidator(Validator):

    def __init__(self, lyrics):
        self.lyrics = lyrics
        self.threshold = 4

    def validate(self, document):
        try:
            selection = document.text
            selected = [int(num) for num in selection.split("-")]

            lines = [line for line in self.lyrics.split("\n")]
            line_count = len(lines)

            if (
                len(selected) != 2
                or selected[0] >= selected[1]
                or selected[0] <= 0
                or selected[1] > line_count
            ):
                raise ValidationError(
                    message="> Invalid range. Ensure the format is 'start-end' and start is less than end.",
                    cursor_position=len(selection),  # Move cursor to end
                )

            portion = lines[selected[0] - 1 : selected[1]]
            selected_lines = [line for line in portion if line != ""]

            if len(selected_lines) < self.threshold:
                raise ValidationError(
                    message=f"> Selection is less than the minimum required lines ({self.threshold}).",
                    cursor_position=len(selection),  # Move cursor to end
                )

            if len(selected_lines) > self.threshold:
                raise ValidationError(
                    message=f"> Selection exceeds the maximum allowed lines ({self.threshold}).",
                    cursor_position=len(selection),  # Move cursor to end
                )

        except ValueError:
            raise ValidationError(
                message="> Invalid input. Ensure you enter two numbers separated by a hyphen.",
                cursor_position=len(document.text),  # Move cursor to end
            )


class LineCountValidator(Validator):

    def validate(self, document):
        lyrics = document.text

        splitted = lyrics.split("\n")

        if len(splitted) > 4 or len(splitted) < 4:
            raise ValidationError(
                message="> Exactly 4 lines must be given, no more, no less.",
                cursor_position=len(document.text),  # Move cursor to end
            )


class LengthValidator(Validator):

    def validate(self, document):
        name = document.text

        if len(name) <= 0:
            raise ValidationError(
                message="> You can't leave the search query empty when searching.",
                cursor_position=len(document.text),  # Move cursor to end
            )

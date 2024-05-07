"""
Generates posters with track info and lyrics.

Imports:
    - os: OS interaction.
    - image: Image manipulation.
    - utils: Utility functions.
    - writing: Text writing on images.
    - PIL: Image processing.
    - dim: Coordinates & Sizes.
"""

import os
import image
import utils
import writing

from PIL import Image
from PIL import ImageDraw

import dim
from utils import font


class Poster:
    """
    This class represents a poster generator for track information and lyrics.

    Attributes:
        save_path (str): The path where the generated posters will be saved.
    """

    def __init__(
            self,
            save_path=os.getcwd(),
    ):
        self.save_path = save_path

    def generate(self,
                 track_info: dict,
                 lyrics: str,
                 accent=False,
                 custom_image=None):
        """
        Generates a poster with track information and lyrics.

        Args:
            track_info (dict): Information about the track.
            lyrics (str): The lyrics of the track.
            accent (bool, optional): Flag indicating whether to highlight accent color in the palette.
            custom_image (str, optional): Path to a custom image to use as the cover. Defaults to None.
        """
        # Open the poster template image
        with Image.open("./assets/banner_v1.png") as poster:
            draw = ImageDraw.Draw(poster)
            COLOR = (50, 47, 48)

            cover_path = track_info["cover"]
            id = track_info["track_id"]
            name = track_info["name"].upper()
            artist = track_info["artist"]
            duration = track_info["duration"]
            label = track_info["label"]

            if custom_image is not None:
                image.crop_to_square(str(custom_image),
                                     "./assets/custom_image.jpg")
                cover_path = "./assets/custom_image.jpg"

            # Open the cover image
            with Image.open(cover_path) as cover:
                cover = cover.resize(dim.S_COVER)

            # Generate the Spotify scan code for the track and resize it.
            image.scannable(id)

            with Image.open("./assets/spotify_code.png") as spotify_code:
                spotify_code = spotify_code.resize(
                    dim.S_SPOTIFY_CODE,
                    Image.Resampling.BICUBIC).convert("RGBA")

            # Paste the cover and the scan image onto the poster
            poster.paste(cover, dim.C_COVER)
            poster.paste(spotify_code, dim.C_SPOTIFY_CODE, spotify_code)

            # Draw the color palette on the poster
            image.draw_palette(draw, cover_path, accent)

            # Write the title (song name and year) on the poster
            writing.heading(draw, dim.C_HEADING, 915, name, COLOR,
                            font("Bold"), dim.S_HEADING)

            # Write the name of the artist and duration on the poster
            writing.draw_text_v2(
                draw,
                dim.C_ARTIST,
                artist,
                COLOR,
                font("Regular"),
                dim.S_ARTIST,
                anchor="ls",
            )
            writing.draw_text_v2(
                draw,
                dim.C_DURATION,
                duration,
                COLOR,
                font("Regular"),
                dim.S_DURATION,
                anchor="rs",
            )

            # Write the lyrics on the poster
            writing.draw_multiline_text_v2(draw,
                                           dim.C_LYRICS,
                                           lyrics,
                                           COLOR,
                                           font("Light"),
                                           dim.S_LYRICS,
                                           anchor="lt")

            # Write the label information on the poster
            writing.draw_multiline_text_v2(draw,
                                           dim.C_LABEL,
                                           label,
                                           COLOR,
                                           font("Regular"),
                                           dim.S_LABEL,
                                           anchor="rt")

            # Create folder to save the poster image
            utils.create_folder()

            # Generate a unique filename for the poster image
            filename = (
                f"{utils.create_filename(name, artist)}_{utils.special_code()}.png"
            )
            # Save the poster image
            poster.save(f"{self.save_path}/{filename}")
            poster.show()

            print(f"☕ • Image saved in the image folder of this repository")

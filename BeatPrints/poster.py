"""
Module: poster.py

Generates poster with track info and lyrics.

Imports:
    - os: Provides OS interaction
    - PIL: Image processing Library
    - utils: Useful utility functions.
    - dim: Cords & Sizes for necessary texts.
    - write: Custom draw.text functions for text handling.
    - image: Provides essential image functions for poster generation.
"""

import os
import dim
import image
import utils
import write

from PIL import Image
from PIL import ImageDraw


class Poster:
    """
    This class represents a poster generator for track information and lyrics.

    Attributes:
        save_path (str): The path where the generated posters will be saved.
    """

    def __init__(
        self,
        save_path=None,
    ):
        self.save_path = save_path

    def generate(self,
                 track_info: dict,
                 lyrics: str,
                 accent=False,
                 custom_image=None,
                 dark_mode=False):
        """
        Creates a poster with track details and lyrics.

        Args:
            track_info (dict): Track details.
            lyrics (str): Track lyrics.
            accent (bool, optional): Adds an accent at the bottom. Defaults to False.
            custom_image (str, optional): Path to a custom cover image. Defaults to None.
            dark_mode (bool, optional): Generates a dark-themed poster. Defaults to False.
        """

        assets_path = os.path.realpath("assets")

        # Selecting the color and theme of the banner
        color, banner = (dim.CL_DARK_MODE,
                         "banner_dark.png") if dark_mode else (
                             dim.CL_LIGHT_MODE, "banner_light.png")

        banner_path = os.path.join(assets_path, "templates", banner)

        # Open the poster template image
        with Image.open(banner_path) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            name = track_info["name"].upper()
            label = track_info["label"]
            artist = track_info["artist"]
            duration = track_info["duration"]
            track_id = track_info["track_id"]
            cover_path = track_info["cover"]

            # If the user wants a custom image...
            if custom_image is not None:
                cover_path = os.path.join(assets_path, "spotify",
                                          "custom_image.jpg")
                image.square_crop(str(custom_image), cover_path)

            # Open the cover image
            with Image.open(cover_path) as cover:
                cover = cover.resize(dim.S_COVER)

            # Generate the Spotify scan code for the track and resize it.
            image.scannable(track_id, dark_mode)
            spotify_code_path = os.path.join(assets_path, "spotify",
                                             "spotify_code.png")

            with Image.open(spotify_code_path) as spotify_code:
                spotify_code = spotify_code.resize(
                    dim.S_SPOTIFY_CODE,
                    Image.Resampling.BICUBIC).convert("RGBA")

            # Paste the cover and the scan image onto the poster
            poster.paste(cover, dim.C_COVER)
            poster.paste(spotify_code, dim.C_SPOTIFY_CODE, spotify_code)

            # Draw the color palette on the poster
            image.draw_palette(draw, cover_path, accent)

            # Write the heading on the poster
            write.heading(draw, dim.C_HEADING, 915, name, color,
                          write.font("Bold"), dim.S_HEADING)

            # Write the name of the artist and duration on the poster
            write.text_v2(
                draw,
                dim.C_ARTIST,
                artist,
                color,
                write.font("Regular"),
                dim.S_ARTIST,
                anchor="ls",
            )
            write.text_v2(
                draw,
                dim.C_DURATION,
                duration,
                color,
                write.font("Regular"),
                dim.S_DURATION,
                anchor="rs",
            )

            # Write the lyrics on the poster
            write.multiline_text_v2(draw,
                                    dim.C_LYRICS,
                                    lyrics,
                                    color,
                                    write.font("Light"),
                                    dim.S_LYRICS,
                                    anchor="lt")

            # Write the label information on the poster
            write.multiline_text_v2(draw,
                                    dim.C_LABEL,
                                    label,
                                    color,
                                    write.font("Regular"),
                                    dim.S_LABEL,
                                    anchor="rt")

            # Generate a unique filename for the poster image
            filename = (
                f"{utils.create_filename(name, artist)}_{utils.special_code()}.png"
            )

            # [ note ] This "save-feature" will be reimplemented later on
            if self.save_path is None:
                path = os.path.dirname(os.path.realpath("."))
                poster_dir = os.path.join(path, "posters")

            else:
                path = os.path.realpath(self.save_path)
                poster_dir = os.path.join(path, "posters")

            if not os.path.exists(poster_dir):
                os.makedirs(poster_dir)

            # Save the poster image in the local repository
            poster.save(os.path.join(poster_dir, filename))
            print(f"✨ Saved image at {poster_dir}/")

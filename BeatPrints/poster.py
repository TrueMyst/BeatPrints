"""
Module: poster.py

Generates posters with track info and lyrics.

Imports:
    - os: OS interaction.
    - PIL: Image processing.

    - dim: Coordinates & Sizes.
    - image: Image manipulation.
    - utils: Utility functions.
    - writing: Text writing on images.
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
                 custom_image=None,
                 dark_mode=False):
        """
        Generates a poster with track information and lyrics.

        Args:
            track_info (dict): Information about the track.
            lyrics (str): The lyrics of the track.
            accent (bool, optional): Flag indicating whether to highlight accent color in the palette.
            custom_image (str, optional): Path to a custom image to use as the cover. Defaults to None.
        """

        banner_path = "./assets/banner_dark.png" if dark_mode else "./assets/banner_light.png"
        color = dim.CL_DARK_MODE if dark_mode else dim.CL_LIGHT_MODE

        # Open the poster template image
        with Image.open(banner_path) as poster:
            poster = poster.convert("RGB")

            draw = ImageDraw.Draw(poster)

            cover_path = track_info["cover"]
            id = track_info["track_id"]
            name = track_info["name"].upper()
            artist = track_info["artist"]
            duration = track_info["duration"]
            label = track_info["label"]

            if custom_image is not None:
                image.square_crop(str(custom_image),
                                  "./assets/spotify/custom_image.jpg")
                cover_path = "./assets/spotify/custom_image.jpg"

            # Open the cover image
            with Image.open(cover_path) as cover:
                cover = cover.resize(dim.S_COVER)

            # Generate the Spotify scan code for the track and resize it.
            image.scannable(id, dark_mode)

            with Image.open(
                    "./assets/spotify/spotify_code.png") as spotify_code:
                spotify_code = spotify_code.resize(
                    dim.S_SPOTIFY_CODE,
                    Image.Resampling.BICUBIC).convert("RGBA")

            # Paste the cover and the scan image onto the poster
            poster.paste(cover, dim.C_COVER)
            poster.paste(spotify_code, dim.C_SPOTIFY_CODE, spotify_code)

            # Draw the color palette on the poster
            image.draw_palette(draw, cover_path, accent)

            # Write the title (song name and year) on the poster
            writing.heading(draw, dim.C_HEADING, 915, name, color,
                            font("Bold"), dim.S_HEADING)

            # Write the name of the artist and duration on the poster
            writing.draw_text_v2(
                draw,
                dim.C_ARTIST,
                artist,
                color,
                font("Regular"),
                dim.S_ARTIST,
                anchor="ls",
            )
            writing.draw_text_v2(
                draw,
                dim.C_DURATION,
                duration,
                color,
                font("Regular"),
                dim.S_DURATION,
                anchor="rs",
            )

            # Write the lyrics on the poster
            writing.draw_multiline_text_v2(draw,
                                           dim.C_LYRICS,
                                           lyrics,
                                           color,
                                           font("Light"),
                                           dim.S_LYRICS,
                                           anchor="lt")

            # Write the label information on the poster
            writing.draw_multiline_text_v2(draw,
                                           dim.C_LABEL,
                                           label,
                                           color,
                                           font("Regular"),
                                           dim.S_LABEL,
                                           anchor="rt")

            # Generate a unique filename for the poster image
            filename = (
                f"{utils.create_filename(name, artist)}_{utils.special_code()}.png"
            )

            if self.save_path != None:
                fn = f"../posters/"

                # Save the poster image in local repository
                os.makedirs(fn)
                poster.save(f"{fn}{filename}")

                print(f"✨ Saved image at {fn}")

            else:
                fn = f"{self.save_path}/posters/"

                # Save the poster image in a custom directory
                os.makedirs(fn)
                poster.save(f"{fn}{filename}")

                print(f"✨ Saved image at {fn}")

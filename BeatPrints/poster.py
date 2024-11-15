"""
Module: poster.py

Generates poster based on the track info and lyrics.
"""

import os, requests

from typing import Optional
from PIL import Image, ImageDraw

from . import image
from . import write
from . import utils

from .consts import *
from .spotify import TrackMetadata
from .errors import PathNotFoundError


class Poster:
    """
    A class to generate and save posters containing track information and lyrics.

    Attributes:
        save_path (str): The directory where the generated posters will be saved.
    """

    def __init__(self, save_path: str):
        """
        Initializes a Poster instance with a specified save directory.

        Args:
            save_path (str): The directory where the posters will be saved.
        """
        self.P_SAVE = save_path

    def generate(
        self,
        metadata: TrackMetadata,
        lyrics: str,
        accent: bool = False,
        dark_mode: bool = False,
        custom_image: Optional[str] = None,
    ) -> None:
        """
        Creates a poster with the track's info and lyrics.

        Args:
            metadata (TrackMetadata): Information about the track.
            lyrics (str): The song lyrics.
            accent (bool, optional): Add a design accent. Defaults to False.
            dark_mode (bool, optional): Use a dark theme. Defaults to False.
            custom_image (str, optional): Path to a custom image. Defaults to None.
        """

        # Check whether the output path exists or not
        if not self.P_SAVE or not os.path.exists(self.P_SAVE):
            raise PathNotFoundError

        # Determine the color and theme of the banner based on the dark mode flag
        color, theme = (
            (CL_DARK_MODE, "banner_dark.png")
            if dark_mode
            else (CL_LIGHT_MODE, "banner_light.png")
        )

        # Define the path for the banner template
        banner_path = os.path.join(P_TEMPLATES, theme)

        # Create a folder called "media" to store our assets
        P_MEDIA = os.path.join(self.P_SAVE, "media")
        os.makedirs(P_MEDIA, exist_ok=True)

        # The path to save the cover image
        cover_path = os.path.join(P_MEDIA, "cover.jpg")

        # Use custom image if provided, otherwise download the cover image
        if custom_image:
            image.crop(custom_image, cover_path)
        else:
            with open(cover_path, "wb") as cover_file:
                cover_file.write(requests.get(metadata.image).content)

        # Adjust the brightness and contrast of the cover image
        image.magicify(cover_path)

        # Generate and resize the Spotify scan code
        scannable_path = image.scannable(metadata.id, P_MEDIA, dark_mode)

        # Preparing the poster :>
        with Image.open(banner_path) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            # Open and resize the cover & the scannable code
            with Image.open(cover_path) as cover:
                cover = cover.resize(S_COVER)

            with Image.open(scannable_path) as scannable:
                scannable = scannable.resize(
                    S_SPOTIFY_CODE, Image.Resampling.BICUBIC
                ).convert("RGBA")

            # Paste the cover and the scannable code onto the poster
            poster.paste(cover, C_COVER)
            poster.paste(scannable, C_SPOTIFY_CODE, scannable)

            # Layout the color palette on the poster
            image.draw_palette(draw, cover_path, accent)

            # Write the heading on the poster
            write.heading(
                draw,
                C_HEADING,
                875,
                metadata.name.upper(),
                color,
                write.font("Bold"),
                S_HEADING,
            )

            # Write the artist name and track duration on the poster
            write.text(
                draw,
                C_ARTIST,
                metadata.artist,
                color,
                write.font("Regular"),
                S_ARTIST,
                anchor="ls",
            )
            write.text(
                draw,
                C_DURATION,
                metadata.duration,
                color,
                write.font("Regular"),
                S_DURATION,
                anchor="rs",
            )

            # Write the lyrics on the poster
            write.text(
                draw,
                C_LYRICS,
                lyrics,
                color,
                write.font("Light"),
                S_LYRICS,
                anchor="lt",
            )

            # Write the label information on the poster
            custom_label = f"{metadata.released}\n{metadata.label}"

            write.text(
                draw,
                C_LABEL,
                custom_label,
                color,
                write.font("Regular"),
                S_LABEL,
                anchor="rt",
            )

            # Generate a unique filename for the poster image
            filename = utils.create_filename(metadata.name, metadata.artist)

            # Save the poster image to the specified directory
            poster.save(os.path.join(self.P_SAVE, filename))
            print(f"✨ {metadata.name} by {metadata.artist}")
            print(f" ╰─ Poster successfully saved in {self.P_SAVE}")

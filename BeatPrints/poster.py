"""
Module: poster.py

Generates poster based on track info and lyrics.

Imports:
    - os: Provides OS interaction.
    - requests: Simplifies HTTP requests.
    - image: Essential image functions to generate posters.
    - consts: Coordinates & sizes for necessary texts.
    - write: Better draw.text().
    - utils: Useful utility functions.
    - typing: Type hinting support.
    - PIL: Image processing library (Pillow).
"""

import os, requests
import image, consts, write, utils

from typing import Dict, Optional
from PIL import Image, ImageDraw


class Poster:
    """
    This class represents a poster generator for track information and lyrics.

    Attributes:
        save (str): The directory where the generated posters will be saved.
    """

    def __init__(self, save: Optional[str] = None):
        """
        Initializes the Poster instance with an optional output directory.

        Args:
            save (str, optional): The directory where the posters will be saved. Defaults to None.
        """
        self.save = save

    def generate(
        self,
        metadata: Dict[str, str],
        lyrics: str,
        accent: bool = False,
        dark_mode: bool = False,
        custom_image: Optional[str] = None,
    ) -> None:
        """
        Generates a poster with track information and lyrics.

        Args:
            metadata (Dict[str, str]): Dictionary containing track metadata.
            lyrics (str): Lyrics of the track.
            accent (bool, optional): Flag to add an accent to the poster. Defaults to False.
            dark_mode (bool, optional): Flag to use dark mode theme. Defaults to False.
            custom_image (str, optional): Path to a custom image for the poster. Defaults to None.
        """
        # Determine the color and theme of the banner based on the dark mode flag
        color, banner_theme = (
            (consts.CL_DARK_MODE, "banner_dark.png")
            if dark_mode
            else (consts.CL_LIGHT_MODE, "banner_light.png")
        )

        # Define the path for the banner template
        banner_path = os.path.join(consts.P_TEMPLATES, banner_theme)

        # Open and prepare the banner template image
        with Image.open(banner_path) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            # Extract important metadata
            track_name = metadata["name"].upper()
            track_label = metadata["label"]
            track_artist = metadata["artist"]
            track_duration = metadata["duration"]
            track_released = metadata["released"]
            track_id = metadata["id"]

            # Create a directory for image assets
            os.makedirs(consts.P_IMAGE, exist_ok=True)

            # Define the path for the cover image
            cover_path = os.path.join(consts.P_IMAGE, "cover.jpg")

            # Use custom image if provided, otherwise download the cover image from metadata
            if custom_image:
                image.crop(custom_image, cover_path)
            else:
                with open(cover_path, "wb") as cover_file:
                    cover_file.write(requests.get(metadata["image"]).content)

            # Adjust the brightness and contrast of the cover image
            image.magicify(cover_path)

            # Open and resize the cover image
            with Image.open(cover_path) as cover:
                cover = cover.resize(consts.S_COVER)

            # Generate and resize the Spotify scan code
            image.scannable(track_id, dark_mode)
            scannable_path = os.path.join(consts.P_IMAGE, "scannable.png")

            with Image.open(scannable_path) as scannable:
                scannable = scannable.resize(
                    consts.S_SPOTIFY_CODE, Image.Resampling.BICUBIC
                ).convert("RGBA")

            # Paste the cover image and Spotify scan code onto the poster
            poster.paste(cover, consts.C_COVER)
            poster.paste(scannable, consts.C_SPOTIFY_CODE, scannable)

            # Draw the color palette on the poster
            image.draw_palette(draw, cover_path, accent)

            # Write the heading on the poster
            write.heading(
                draw,
                consts.C_HEADING,
                875,
                track_name,
                color,
                write.font("Bold"),
                consts.S_HEADING,
            )

            # Write the artist name and track duration on the poster
            write.text_v2(
                draw,
                consts.C_ARTIST,
                track_artist,
                color,
                write.font("Regular"),
                consts.S_ARTIST,
                anchor="ls",
            )
            write.text_v2(
                draw,
                consts.C_DURATION,
                track_duration,
                color,
                write.font("Regular"),
                consts.S_DURATION,
                anchor="rs",
            )

            # Write the lyrics on the poster
            write.multiline_text_v2(
                draw,
                consts.C_LYRICS,
                lyrics,
                color,
                write.font("Light"),
                consts.S_LYRICS,
                anchor="lt",
            )

            # Write the label information on the poster
            custom_label = f"{track_released}\n{track_label}"

            write.multiline_text_v2(
                draw,
                consts.C_LABEL,
                custom_label,
                color,
                write.font("Regular"),
                consts.S_LABEL,
                anchor="rt",
            )

            # Generate a unique filename for the poster image
            filename = utils.create_filename(track_name, track_artist)

            # Determine the directory for saving the poster
            poster_dir = os.path.join(
                self.save or os.path.dirname(os.path.realpath(".")), "posters"
            )
            os.makedirs(poster_dir, exist_ok=True)

            # Save the poster image to the specified directory
            poster.save(os.path.join(poster_dir, filename))
            print(f"✨ Saved image at {poster_dir}")

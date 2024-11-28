"""
Module: poster.py

Generates poster based on the track info and lyrics.
"""

import os, requests

from typing import Optional
from PIL import Image, ImageDraw, ImageFont

from . import image
from . import write
from . import utils

from .consts import *
from .spotify import TrackMetadata, AlbumMetadata
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
        self.P_MEDIA = os.path.join(save_path, "media")

    def _setup_media_dir(self):
        """
        Creates and cleans up the media directory.
        """
        # Remove existing media directory if it exists
        if os.path.exists(self.P_MEDIA):
            for file in os.listdir(self.P_MEDIA):
                os.remove(os.path.join(self.P_MEDIA, file))
            os.rmdir(self.P_MEDIA)
        
        # Create fresh media directory
        os.makedirs(self.P_MEDIA, exist_ok=True)

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

        # Setup media directory
        self._setup_media_dir()

        # Determine the color and theme of the banner based on the dark mode flag
        color, theme = (
            (CL_DARK_MODE, "banner_dark.png")
            if dark_mode
            else (CL_LIGHT_MODE, "banner_light.png")
        )

        # Define the path for the banner template
        banner_path = os.path.join(P_TEMPLATES, theme)

        # The path to save the cover image
        cover_path = os.path.join(self.P_MEDIA, "cover.jpg")

        # Use custom image if provided, otherwise download the cover image
        if custom_image:
            image.crop(custom_image, cover_path)
        else:
            with open(cover_path, "wb") as cover_file:
                cover_file.write(requests.get(metadata.image).content)

        # Adjust the brightness and contrast of the cover image
        image.magicify(cover_path)

        # Generate and resize the Spotify scan code
        scannable_path = image.scannable(metadata.id, self.P_MEDIA, dark_mode)

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

    def generate_album(
        self,
        metadata: AlbumMetadata,
        accent: bool = False,
        dark_mode: bool = False,
        custom_image: Optional[str] = None,
    ) -> None:
        """
        Creates a poster with album info and track listing.

        Args:
            metadata (AlbumMetadata): Information about the album
            accent (bool, optional): Add a design accent. Defaults to False.
            dark_mode (bool, optional): Use a dark theme. Defaults to False. 
            custom_image (str, optional): Path to a custom image. Defaults to None.
        """
        # Most of the code is similar to generate() but handles track listing instead of lyrics
        
        # Check path exists
        if not self.P_SAVE or not os.path.exists(self.P_SAVE):
            raise PathNotFoundError

        # Setup media directory
        self._setup_media_dir()

        # Determine theme
        color, theme = (CL_DARK_MODE, "banner_dark.png") if dark_mode else (CL_LIGHT_MODE, "banner_light.png")
        banner_path = os.path.join(P_TEMPLATES, theme)

        # The path to save the cover image
        cover_path = os.path.join(self.P_MEDIA, "cover.jpg")
        if custom_image:
            image.crop(custom_image, cover_path)
        else:
            with open(cover_path, "wb") as cover_file:
                cover_file.write(requests.get(metadata.image).content)
        image.magicify(cover_path)

        # Generate scannable code
        scannable_path = image.scannable(metadata.id, self.P_MEDIA, dark_mode, is_album=True)

        with Image.open(banner_path) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            # Paste cover and scannable
            with Image.open(cover_path) as cover:
                cover = cover.resize(S_COVER)
            with Image.open(scannable_path) as scannable:
                scannable = scannable.resize(S_SPOTIFY_CODE, Image.Resampling.BICUBIC).convert("RGBA")
                
            poster.paste(cover, C_COVER)
            poster.paste(scannable, C_SPOTIFY_CODE, scannable)

            # Draw color palette
            image.draw_palette(draw, cover_path, accent)

            # Write album info
            write.heading(
                draw, C_HEADING, 875,
                metadata.name.upper(), color,
                write.font("Bold"), S_HEADING
            )

            write.text(
                draw, C_ARTIST,
                metadata.artist, color,
                write.font("Regular"), S_ARTIST,
                anchor="ls"
            )

            # Calculate columns and track distribution
            track_count = len(metadata.tracks)
            
            # Force columns based on track count
            if track_count <= 6:
                columns = 1
                track_font_size = 32
                column_positions = [(C_LYRICS[0], C_LYRICS[1])]
            elif track_count <= 12:
                columns = 2
                track_font_size = 30
                column_positions = [
                    (C_LYRICS[0], C_LYRICS[1]),
                    (C_LYRICS[0] + 450, C_LYRICS[1])
                ]
            else:
                columns = 3
                track_font_size = 28
                column_positions = [
                    (C_LYRICS[0], C_LYRICS[1]),
                    (C_LYRICS[0] + 325, C_LYRICS[1]),
                    (C_LYRICS[0] + 650, C_LYRICS[1])
                ]
            
            # Split tracks evenly between columns
            tracks_per_column = (track_count + columns - 1) // columns
            track_columns = []
            
            for col in range(columns):
                start_idx = col * tracks_per_column
                end_idx = min((col + 1) * tracks_per_column, track_count)
                
                # Format tracks for this column
                column_tracks = [
                    f"{str(i+1).rjust(2)}. {metadata.tracks[i]}"
                    for i in range(start_idx, end_idx)
                ]
                track_columns.append("\n".join(column_tracks))
            
            # Write each column
            for column_text, position in zip(track_columns, column_positions):
                write.text(
                    draw, 
                    position,
                    column_text, 
                    color,
                    write.font("Light"), 
                    track_font_size,
                    anchor="lt",
                    spacing=0
                )

            # Write label info
            write.text(
                draw, C_LABEL,
                f"{metadata.released}\n{metadata.label}", color,
                write.font("Regular"), S_LABEL,
                anchor="rt"
            )

            # Save poster
            filename = utils.create_filename(metadata.name, metadata.artist)
            poster.save(os.path.join(self.P_SAVE, filename))
            print(f"✨ {metadata.name} by {metadata.artist}")
            print(f" ╰─ Album poster successfully saved in {self.P_SAVE}")

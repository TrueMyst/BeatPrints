"""
Module: poster.py

Generates posters based on track or album information.
"""

import os

from pathlib import Path
from typing import Optional, Union

from PIL import Image, ImageDraw

from .consts import *
from . import image, write
from .utils import filename, organize_tracks

from .errors import ThemeNotFoundError
from .spotify import TrackMetadata, AlbumMetadata


class Poster:
    """
    A class for generating and saving posters containing track or album information.
    """

    def __init__(self, save_to: str):
        """
        Initializes the Poster instance.

        Args:
            save_to (str): Path where posters will be saved.
        """
        self.save_to = Path(save_to).expanduser().resolve()

    def _add_common_text(
        self,
        draw: ImageDraw.ImageDraw,
        metadata: Union[TrackMetadata, AlbumMetadata],
        color: tuple,
    ):
        """
        Adds common text like title, artist, and label info.

        Args:
            draw (ImageDraw.ImageDraw): Draw context.
            metadata: Metadata containing the required text.
            color (tuple): Text color.
        """
        # Add heading (track or album name) in bold
        write.heading(
            draw,
            C_HEADING,
            S_MAX_HEADING_WIDTH,
            metadata.name.upper(),
            color,
            write.font("Bold"),
            S_HEADING,
        )

        # Add artist name
        write.text(
            draw,
            C_ARTIST,
            metadata.artist,
            color,
            write.font("Regular"),
            S_ARTIST,
            anchor="ls",
        )
        # Add release year and label info
        write.text(
            draw,
            C_LABEL,
            f"{metadata.released}\n{metadata.label}",
            color,
            write.font("Regular"),
            S_LABEL,
            anchor="rt",
        )

    def track(
        self,
        metadata: TrackMetadata,
        lyrics: str,
        accent: bool = False,
        theme: THEME_OPTS = "Light",
        custom_cover: Optional[str] = None,
    ) -> None:
        """
        Generates a poster for a track, which includes lyrics.

        Args:
            metadata (TrackMetadata): Metadata containing details about the track.
            lyrics (str): The lyrics of the track.
            accent (bool, optional): Flag to add an accent at the bottom of the poster. Defaults to False.
            theme (Literal, optional): Specifies the theme to use. Must be one of "Light", "Dark", "Catppuccin", "Gruvbox", "Nord", "RosePine", or "Everforest".  Defaults to "Light".
            custom_cover (str, optional): Path to a custom cover image. Defaults to None.
        """

        # Check if the theme mentioned is valid or not
        if theme not in THEMES:
            raise ThemeNotFoundError

        # Get theme colors and template for the poster
        color, template = image.get_theme(theme)

        # Get cover art and spotify scannable code
        cover = image.cover(metadata.image, custom_cover)
        scannable = image.scannable(metadata.id, theme)

        with Image.open(template) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            # Paste the cover and scannable Spotify code
            poster.paste(cover, C_COVER)
            poster.paste(scannable, C_SPOTIFY_CODE, scannable)

            # Optionally add a color palette or accent design
            image.draw_palette(draw, cover, accent)

            # Add common track information (name, artist, etc.)
            self._add_common_text(draw, metadata, color)

            # Add track duration and lyrics to the poster
            write.text(
                draw,
                C_DURATION,
                metadata.duration,
                color,
                write.font("Regular"),
                S_DURATION,
                anchor="rs",
            )
            write.text(
                draw,
                C_LYRICS,
                lyrics,
                color,
                write.font("Light"),
                S_LYRICS,
                anchor="lt",
            )

            # Save the generated poster with a unique filename
            name = filename(metadata.name, metadata.artist)
            poster.save(os.path.join(self.save_to, name))

            print(
                f"✨ Poster for {metadata.name} by {metadata.artist} saved to {self.save_to}"
            )

    def album(
        self,
        metadata: AlbumMetadata,
        indexing: bool = False,
        accent: bool = False,
        theme: THEME_OPTS = "Light",
        custom_cover: Optional[str] = None,
    ) -> None:
        """
        Generates a poster for an album, which includes track listing.

        Args:
            metadata (AlbumMetadata): Metadata containing details about the album.
            indexing (bool, optional): Flag to add index numbers to the tracks. Defaults to False.
            accent (bool, optional): Flag to add an accent at the bottom of the poster. Defaults to False.
            theme (Literal, optional): Specifies the theme to use. Must be one of "Light", "Dark", "Catppuccin", "Gruvbox", "Nord", "RosePine", or "Everforest". Defaults to "Light".
            custom_cover (str, optional): Path to a custom cover image. Defaults to None.
        """

        # Check if the theme mentioned is valid or not
        if theme not in THEMES:
            raise ThemeNotFoundError

        # Get theme colors and template for the poster
        color, template = image.get_theme(theme)

        # Get cover art and spotify scannable code
        cover = image.cover(metadata.image, custom_cover)
        scannable = image.scannable(metadata.id, theme, is_album=True)

        with Image.open(template) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            # Paste the album cover and scannable Spotify code
            poster.paste(cover, C_COVER)
            poster.paste(scannable, C_SPOTIFY_CODE, scannable)

            # Optionally add a color palette or design accents
            image.draw_palette(draw, cover, accent)

            # Add common album information (name, artist, etc.)
            self._add_common_text(draw, metadata, color)

            # Album's Tracks
            tracks = metadata.tracks

            # Organize the tracklist and render it on the poster
            tracklist, track_widths = organize_tracks(tracks, indexing)

            # Starting Position
            x, y = C_TRACKS

            # Render the tracklist, adjusting the position for each column
            for track_column, column_width in zip(tracklist, track_widths):
                write.text(
                    draw,
                    (x, y),
                    "\n".join(track_column),
                    color,
                    write.font("Light"),
                    S_TRACKS,
                    anchor="lt",
                    spacing=2,
                )
                x += column_width + S_SPACING  # Adjust x for next column

            # Save the generated album poster with a unique filename
            name = filename(metadata.name, metadata.artist)
            poster.save(os.path.join(self.save_to, name))
            print(
                f"✨ Album poster for {metadata.name} by {metadata.artist} saved to {self.save_to}"
            )

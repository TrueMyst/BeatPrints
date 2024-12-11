"""
Module: poster.py

Generate posters based on track or albums.
"""

import os
import random
from typing import Optional, Union

from PIL import Image, ImageDraw

from . import image, write, utils
from .consts import *
from .spotify import TrackMetadata, AlbumMetadata


class Poster:
    """
    A class to generate and save posters containing track or album information.

    Attributes:
        save_to (str): Directory where generated posters will be saved.
    """

    def __init__(self, save_to: str):
        """
        Initializes the Poster instance.

        Args:
            save_to (str): Path where posters will be saved.
        """
        self.save_to = os.path.realpath(os.path.expanduser(save_to))

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
        write.heading(
            draw,
            C_HEADING,
            875,
            metadata.name.upper(),
            color,
            write.font("Bold"),
            S_HEADING,
        )
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
        dark_theme: bool = False,
        custom_cover: Optional[str] = None,
    ) -> None:
        """
        Generates a track poster with lyrics, cover, and scannable code.

        Args:
            metadata (TrackMetadata): Track details.
            lyrics (str): Track lyrics.
            accent (bool): Flag to add design accents.
            dark_theme (bool): Flag for dark theme.
            custom_cover (Optional[str]): Path to custom cover.
        """

        # Get theme colors and template
        color, template = image.get_theme(dark_theme)

        # Get cover art and scannable code
        cover = image.cover(metadata.image, custom_cover)
        scannable = image.scannable(metadata.id, dark_theme)

        # Open and prepare poster
        with Image.open(template) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            # Paste cover and scannable code
            poster.paste(cover, C_COVER)
            poster.paste(scannable, C_SPOTIFY_CODE, scannable)

            # Add color palette or design accents
            image.draw_palette(draw, cover, accent)

            # Add common text
            self._add_common_text(draw, metadata, color)

            # Add duration and lyrics
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

            # Save the poster
            name = utils.filename(metadata.name, metadata.artist)
            poster.save(os.path.join(self.save_to, name))

            print(
                f"✨ Poster for {metadata.name} by {metadata.artist} saved to {self.save_to}"
            )

    def album(
        self,
        metadata: AlbumMetadata,
        accent: bool = False,
        dark_theme: bool = False,
        indexing: bool = False,
        custom_cover: Optional[str] = None,
    ) -> None:
        """
        Generates an album poster with album info and track listing.

        Args:
            metadata (AlbumMetadata): Album details.
            accent (bool): Flag to add design accents.
            dark_theme (bool): Flag for dark theme.
            indexing (bool): Flag to add index numbers to tracks.
            custom_cover (Optional[str]): Path to custom cover.
        """

        # Get theme and cover
        color, template_path = image.get_theme(dark_theme)
        cover = image.cover(metadata.image, custom_cover)
        scannable = image.scannable(metadata.id, dark_theme, is_album=True)

        # Open and prepare poster
        with Image.open(template_path) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            # Paste cover and scannable code
            poster.paste(cover, C_COVER)
            poster.paste(scannable, C_SPOTIFY_CODE, scannable)

            # Add color palette or design accents
            image.draw_palette(draw, cover, accent)

            # Add common text
            self._add_common_text(draw, metadata, color)

            # Shuffle and optionally index tracks
            tracks = metadata.tracks[:]
            random.shuffle(tracks)
            if indexing:
                tracks = [f"{i + 1}. {track}" for i, track in enumerate(tracks)]

            # Organize and render tracks
            tracklist, track_widths = utils.organize_tracks(tracks)
            x, y = C_TRACKS

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

            # Save the poster
            name = utils.filename(metadata.name, metadata.artist)
            poster.save(os.path.join(self.save_to, name))
            print(
                f"✨ Album poster for {metadata.name} by {metadata.artist} saved to {self.save_to}"
            )

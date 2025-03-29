"""
Module: poster.py

Generates posters based on track or album information.
"""

import os

from pathlib import Path
from typing import Optional, Tuple, Union

from PIL import Image, ImageDraw

from BeatPrints import image, write
from BeatPrints.utils import filename, organize_tracks

from BeatPrints.errors import ThemeNotFoundError
from BeatPrints.spotify import TrackMetadata, AlbumMetadata
from BeatPrints.consts import Size, Position, ThemesSelector

# Initialize the components
s = Size()
p = Position()
t = ThemesSelector()


class Poster:
    """
    A class for generating and saving posters containing track or album information.

    Args:
        output (str): Path where posters will be saved.
    """

    def __init__(self, output: str):
        """
        Initializes the Poster instance.
        """
        self.save_to = Path(output).expanduser().resolve()

    def _draw_template(
        self,
        draw: ImageDraw.ImageDraw,
        metadata: Union[TrackMetadata, AlbumMetadata],
        color: Tuple[int, int, int],
    ):
        """
        Adds text like title, artist, and label info.

        Args:
            draw (ImageDraw.ImageDraw): Draw context.
            metadata (Union[TrackMetadata, AlbumMetadata]): Metadata containing the required text.
            color (Tuple[int, int, int]): Text color.
        """
        # Add heading (track or album name) in bold
        write.heading(
            draw,
            p.HEADING,
            s.HEADING_WIDTH,
            metadata.name.upper(),
            color,
            write.font("Bold"),
            s.HEADING,
        )

        # Add artist name
        write.text(
            draw,
            p.ARTIST,
            metadata.artist,
            color,
            write.font("Regular"),
            s.ARTIST,
            anchor="ls",
        )
        # Add release year and label info
        write.text(
            draw,
            p.LABEL,
            f"{metadata.released}\n{metadata.label}",
            color,
            write.font("Regular"),
            s.LABEL,
            anchor="rt",
        )

    def track(
        self,
        metadata: TrackMetadata,
        lyrics: str,
        accent: bool = False,
        theme: ThemesSelector.Options = "Light",
        pcover: Optional[str] = None,
    ) -> None:
        """
        Generates a poster for a track, which includes lyrics.

        Args:
            metadata (TrackMetadata): Track's Metadata.
            lyrics (str): The lyrics of the track.
            accent (bool, optional): Adds an accent at the bottom of the poster. Defaults to False.
            theme (ThemesSelector.Options, optional): Specifies the theme to use. Must be one of "Light", "Dark", "Catppuccin", "Gruvbox", "Nord", "RosePine", or "Everforest".  Defaults to "Light".
            pcover (Optional[str]): Path to a custom cover image. Defaults to None.
        """

        # Check if the theme is valid or not
        if theme not in t.THEMES:
            raise ThemeNotFoundError

        # Get theme and template for the poster
        color, template = image.get_theme(theme)

        # Get cover art and scancode
        cover = image.cover(metadata.image, pcover)
        scannable = image.scannable(metadata.id, theme, "track")

        with Image.open(template) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            # Paste the cover and scancode
            poster.paste(cover, p.COVER)
            poster.paste(scannable, p.SCANCODE, scannable)

            # Add an accent at the bottom if True
            image.draw_palette(draw, cover, accent)

            # Add the track's metadata
            self._draw_template(draw, metadata, color)

            # Add the track's duration and lyrics to the poster
            write.text(
                draw,
                p.DURATION,
                metadata.duration,
                color,
                write.font("Regular"),
                s.DURATION,
                anchor="rs",
            )
            write.text(
                draw,
                p.LYRICS,
                lyrics,
                color,
                write.font("Light"),
                s.LYRICS,
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
        theme: ThemesSelector.Options = "Light",
        pcover: Optional[str] = None,
    ) -> None:
        """
        Generates a poster for an album, which includes track listing.

        Args:
            metadata (AlbumMetadata): Metadata containing details about the album.
            indexing (bool, optional): Add index numbers to the tracks. Defaults to False.
            accent (bool, optional): Add an accent at the bottom of the poster. Defaults to False.
            theme (ThemesSelector.Options, optional): Specifies the theme to use. Must be one of "Light", "Dark", "Catppuccin", "Gruvbox", "Nord", "RosePine", or "Everforest". Defaults to "Light".
            pcover (Optional[str]): Path to a custom cover image. Defaults to None.
        """

        # Check if the theme mentioned is valid or not
        if theme not in t.THEMES:
            raise ThemeNotFoundError

        # Get theme colors and template for the poster
        color, template = image.get_theme(theme)

        # Get cover art and spotify scannable code
        cover = image.cover(metadata.image, pcover)
        scannable = image.scannable(metadata.id, theme, "album")

        with Image.open(template) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            # Paste the album cover and scannable Spotify code
            poster.paste(cover, p.COVER)
            poster.paste(scannable, p.SCANCODE, scannable)

            # Optionally add a color palette or design accents
            image.draw_palette(draw, cover, accent)

            # Add album information (name, artist, etc.)
            self._draw_template(draw, metadata, color)

            # Album's Tracks
            tracks = metadata.tracks

            # Organize the tracklist and render it on the poster
            tracklist, track_widths = organize_tracks(tracks, indexing)

            # Starting Position
            x, y = p.TRACKS

            # Render the tracklist, adjusting the position for each column
            for track_column, column_width in zip(tracklist, track_widths):
                write.text(
                    draw,
                    (x, y),
                    "\n".join(track_column),
                    color,
                    write.font("Light"),
                    s.TRACKS,
                    anchor="lt",
                    spacing=2,
                )
                x += column_width + s.SPACING  # Adjust x for next column

            # Save the generated album poster with a unique filename
            name = filename(metadata.name, metadata.artist)
            poster.save(os.path.join(self.save_to, name))
            print(
                f"✨ Album poster for {metadata.name} by {metadata.artist} saved to {self.save_to}"
            )

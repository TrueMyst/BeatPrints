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
from BeatPrints.consts import Size, Position, ThemesSelector, SizeA4, PositionA4

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
        A4: bool = False,
    ):
        """
        Adds text like title, artist, and label info.

        Args:
            draw (ImageDraw.ImageDraw): Draw context.
            metadata (Union[TrackMetadata, AlbumMetadata]): Metadata containing the required text.
            color (Tuple[int, int, int]): Text color.
        """
        if A4:
            print("init the draw temp")
            s = SizeA4()
            p = PositionA4()
        elif not A4:
            s = Size()
            p = Position()

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
        a4: bool = False,
    ) -> None:
        """
        Generates a poster for a track, which includes lyrics.

        Args:
            metadata (TrackMetadata): Track's Metadata.
            lyrics (str): The lyrics of the track.
            accent (bool, optional): Adds an accent at the bottom of the poster. Defaults to False.
            theme (ThemesSelector.Options, optional): Specifies the theme to use. Must be one of "Light", "Dark", "Catppuccin", "Gruvbox", "Nord", "RosePine", or "Everforest".  Defaults to "Light".
            pcover (Optional[str]): Path to a custom cover image. Defaults to None.
            a4 (bool, optional): Generate poster in A4 size (2480x3508). Defaults to True.
        """
        # Initialize size and position constants based on poster format
        if a4:  
            s = SizeA4()
            p = PositionA4()
        else:
            s = Size()
            p = Position()

        # Check if the theme is valid or not
        if theme not in t.THEMES:
            raise ThemeNotFoundError

        # Get theme and A4 template path for the poster
        color, template_path = image.get_theme(theme, A4=a4)
        # Adjust constants based on poster size
        # Get cover art and scancode sized for A4
        cover = image.cover(metadata.image, pcover, A4=a4)
        scannable = image.scannable(metadata.id, theme, "track", A4=a4)

        # Load the A4 template with beautiful original design elements
        with Image.open(template_path) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            # Paste the cover and scancode at A4-native positions
            poster.paste(cover, p.COVER)
            poster.paste(scannable, p.SCANCODE, scannable)

            # Add an accent at the bottom if True
            image.draw_palette(draw, cover, accent, A4=a4)

            # Add the track's metadata using A4-native sizes and positions
            self._draw_template(draw, metadata, color, A4=a4)

            # Add the track's duration and lyrics using A4-native sizes
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

            # Save the A4 poster with preserved original design elements
            name = filename(metadata.name, metadata.artist)
            poster.save(os.path.join(self.save_to, name))

            if a4:
                print(
                f"✨ Poster for {metadata.name} by {metadata.artist} saved to {self.save_to} (A4: 2480×3508)"
                )
            else:
                print(
                    f"✨ Poster for {metadata.name} by {metadata.artist} saved to {self.save_to} 2280×3480"
                )

    def album(
        self,
        metadata: AlbumMetadata,
        indexing: bool = False,
        accent: bool = False,
        theme: ThemesSelector.Options = "Light",
        pcover: Optional[str] = None,
        a4: bool = False,
    ) -> None:
        """
        Generates a poster for an album, which includes track listing.

        Args:
            metadata (AlbumMetadata): Metadata containing details about the album.
            indexing (bool, optional): Add index numbers to the tracks. Defaults to False.
        """
        # Initialize size and position constants based on poster format
        if a4:  
            s = SizeA4()
            p = PositionA4()
        elif not a4:
            s = Size()
            p = Position()

        # Check if the theme mentioned is valid or not
        if theme not in t.THEMES:
            raise ThemeNotFoundError

        # Get theme colors and A4 template path for the poster
        color, template_path = image.get_theme(theme, A4=a4)

        # Get cover art and spotify scannable code sized for A4
        cover = image.cover(metadata.image, pcover, A4=a4)
        scannable = image.scannable(metadata.id, theme, "album", A4=a4)

        # Load the A4 template with beautiful original design elements
        with Image.open(template_path) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            # Paste the album cover and scannable Spotify code at A4-native positions
            poster.paste(cover, p.COVER)
            poster.paste(scannable, p.SCANCODE, scannable)

            # Optionally add a color palette or design accents
            image.draw_palette(draw, cover, accent, A4=a4)

            # Add album information using A4-native sizes and positions
            self._draw_template(draw, metadata, color, A4=a4)

            # Album's Tracks
            tracks = metadata.tracks

            # Organize the tracklist and render it on the poster using A4-native sizing
            tracklist, track_widths = organize_tracks(tracks, indexing)

            # Starting Position (A4-native)
            x, y = p.TRACKS

            # Render the tracklist using A4-native font sizes and spacing
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
                x += column_width + s.SPACING  # A4-native spacing

            # Save the A4 album poster with preserved original design elements
            name = filename(metadata.name, metadata.artist)
            poster.save(os.path.join(self.save_to, name))
            if a4:
                print(
                f"✨ Poster for {metadata.name} by {metadata.artist} saved to {self.save_to} (A4: 2480×3508)"
                )
            else:
                print(
                    f"✨ Poster for {metadata.name} by {metadata.artist} saved to {self.save_to} 2280×3480"
                )

"""
Module: consts.py

Stores all the coordinates, sizes, colors, and paths
needed for positioning text and images on the poster.
"""

import os
import random

from typing import Literal, TypeAlias


class Size:
    # Heading's Width (Max)
    HEADING_WIDTH = 1760

    # Resolution Size
    COVER = (2040, 2040)
    SCANCODE = (660, 170)

    # Track/Album Metadata
    TRACKS = 70
    HEADING = 160
    ARTIST = 120
    DURATION = 90
    LYRICS = 84
    LABEL = 60

    # Album's Tracklist
    MAX_ROWS = 5
    MAX_WIDTH = 2040

    # Space between texts
    SPACING = 70

    # Color Palette
    PL_WIDTH = 340
    PL_HEIGHT = 2325


class Position:
    COVER = (120, 120)
    HEADING = (120, 2550)
    ARTIST = (120, 2700)
    LYRICS = (120, 2790)
    TRACKS = (120, 2780)
    LABEL = (2160, 3230)
    DURATION = (2160, 2550)
    PALETTE = (120, 2240)
    ACCENT = (0, 3440, 2280, 3480)
    SCANCODE = (90, 3220)


class Color:
    # Default Themes
    DARK = (193, 189, 178)
    LIGHT = (50, 47, 48)

    # Extra Themes
    CATPPUCCIN = (205, 214, 244)
    GRUVBOX = (221, 199, 161)
    NORD = (216, 222, 233)
    ROSEPINE = (224, 222, 244)
    EVERFOREST = (211, 198, 170)

    # Spotify Scancode
    WHITE = (255, 255, 255, 255)
    TRANSPARENT = (0, 0, 0, 0)


class ThemesSelector:
    THEMES = {
        "Light": Color.LIGHT,
        "Dark": Color.DARK,
        "Catppuccin": Color.CATPPUCCIN,
        "Gruvbox": Color.GRUVBOX,
        "Nord": Color.NORD,
        "RosePine": Color.ROSEPINE,
        "Everforest": Color.EVERFOREST,
    }

    Options: TypeAlias = Literal[
        "Light", "Dark", "Catppuccin", "Gruvbox", "Nord", "RosePine", "Everforest"
    ]


class FilePath:
    FULLPATH = os.path.join(os.path.dirname(__file__))
    ASSETS = os.path.join(FULLPATH, "assets")

    FONTS = os.path.join(ASSETS, "fonts")
    TEMPLATES = os.path.join(ASSETS, "templates")


class Instrumental:
    PLACEHOLDER = random.choice(
        [
            "woosh- instrumental vibes ahead!",
            "here's a track with some serious feels!",
            "the melody speaks for itself!",
            "all melody, no lyrics!",
            "it's a wordless masterpiece!",
        ]
    )

    DESC = (
        f"""(\\_/)\n( •.•) mmm, this is an instrumental track !!!\n/> {PLACEHOLDER}"""
    )

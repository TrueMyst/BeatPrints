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


class SizeA4:
    # A4 Canvas Size (300 DPI) - Native Resolution
    A4_WIDTH = 2480
    A4_HEIGHT = 3508
    
    # Heading's Width (Max) - Scaled for A4: 1760 * 1.0877 = 1914
    HEADING_WIDTH = 1914

    # Resolution Size - Scaled for A4
    COVER = (2219, 2062)  # 2040 * 1.0877 = 2219
    SCANCODE = (718, 171)  # 660 * 1.0877 = 718, 170 * 1.0080 = 171

    # Track/Album Metadata - Font sizes scaled for A4
    TRACKS = 76      # 70 * 1.0877 = 76
    HEADING = 174    # 160 * 1.0877 = 174
    ARTIST = 131     # 120 * 1.0877 = 131
    DURATION = 98    # 90 * 1.0877 = 98
    LYRICS = 91      # 84 * 1.0877 = 91
    LABEL = 65       # 60 * 1.0877 = 65

    # Album's Tracklist
    MAX_ROWS = 5
    MAX_WIDTH = 2219  # 2040 * 1.0877 = 2219

    # Space between texts - Scaled for A4
    SPACING = 76     # 70 * 1.0877 = 76

    # Color Palette - Scaled for A4
    PL_WIDTH = 370   # 340 * 1.0877 = 370
    PL_HEIGHT = 2344 # 2325 * 1.0080 = 2344


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

class PositionA4:
    # All positions scaled for A4 canvas (X * 1.0877, Y * 1.0080)
    COVER = (131, 121)         # (120 * 1.0877, 120 * 1.0080)
    HEADING = (131, 2570)      # (120 * 1.0877, 2550 * 1.0080)
    ARTIST = (131, 2722)       # (120 * 1.0877, 2700 * 1.0080)
    LYRICS = (131, 2812)       # (120 * 1.0877, 2790 * 1.0080)
    TRACKS = (131, 2802)       # (120 * 1.0877, 2780 * 1.0080)
    LABEL = (2349, 3257)       # (2160 * 1.0877, 3230 * 1.0080)
    DURATION = (2349, 2570)    # (2160 * 1.0877, 2550 * 1.0080)
    PALETTE = (131, 2258)      # (120 * 1.0877, 2240 * 1.0080)
    ACCENT = (0, 3468, 2480, 3508)  # (0, 3440 * 1.0080, 2280 * 1.0877, 3480 * 1.0080)
    SCANCODE = (98, 3246)      # (90 * 1.0877, 3220 * 1.0080)


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

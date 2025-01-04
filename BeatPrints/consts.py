"""
Module: consts.py

Contains all the necessary co-ordinates that'll
be needed to place the texts/images on the poster.

Prefixes
---------
S = Size
C = Cords
P = Path
PL = Palette
CL = Color
T = Text
"""

import os
from typing import Literal

MAX_ROWS = 5
MAX_WIDTH = 2040

S_MAX_HEADING_WIDTH = 1760
S_TRACKS = 70
S_SPACING = 90
S_COVER = (2040, 2040)
S_SPOTIFY_CODE = (660, 170)
S_HEADING = 160
S_ARTIST = 120
S_DURATION = 90
S_LYRICS = 84
S_LABEL = 60

C_COVER = (120, 120)
C_HEADING = (120, 2550)
C_ARTIST = (120, 2700)
C_LYRICS = (120, 2790)
C_TRACKS = (120, 2780)
C_LABEL = (2160, 3230)
C_DURATION = (2160, 2550)
C_PALETTE = (120, 2240)
C_ACCENT = (0, 3440, 2280, 3480)
C_SPOTIFY_CODE = (90, 3220)

PL_BOX_WIDTH = 340
PL_BOX_HEIGHT = 2325

CL_FONT_DARK = (193, 189, 178)
CL_FONT_LIGHT = (50, 47, 48)
CL_FONT_CATPPUCCIN = (205, 214, 244)
CL_FONT_GRUVBOX = (221, 199, 161)
CL_FONT_NORD = (216, 222, 233)
CL_FONT_ROSEPINE = (224, 222, 244)
CL_FONT_EVERFOREST = (211, 198, 170)

THEMES = {
    "Light": CL_FONT_LIGHT,
    "Dark": CL_FONT_DARK,
    "Catppuccin": CL_FONT_CATPPUCCIN,
    "Gruvbox": CL_FONT_GRUVBOX,
    "Nord": CL_FONT_NORD,
    "RosePine": CL_FONT_ROSEPINE,
    "Everforest": CL_FONT_EVERFOREST,
}

THEME_OPTS = Literal[
    "Light",
    "Dark",
    "Catppuccin",
    "Gruvbox",
    "Nord",
    "RosePine",
    "Everforest",
]

CL_WHITE = (255, 255, 255, 255)
CL_TRANSPARENT = (0, 0, 0, 0)

P_FULLPATH = os.path.join(os.path.dirname(__file__))
P_ASSETS = os.path.join(P_FULLPATH, "assets")
P_FONTS = os.path.join(P_ASSETS, "fonts")
P_TEMPLATES = os.path.join(P_ASSETS, "templates")

T_INSTRUMENTAL = [
"""\
(\\_/)
( •.•) meow~ this is an instrumental track~!!
/> Zero words, all vibes?
 
""",
"""\
(\\_/)
( •.•) woosh~ instrumental vibes ahead~!!
/> No words, all melody~
 
""",
"""\
(\\_/)
( •.•) no words, just vibes~!!
/> Instrumental track ahead~!!
 
""",
"""\
(\\_/)
( •.•) here's a track full of feels~!!
/> Let the rhythm carry you~
 
""",
"""\
(\\_/)
( •.•) instrumental groove incoming~!!
/> No lyrics, just soundscapes~
 
""",
"""\
(\\_/)
( •.•) the melody speaks for itself~!!
/> All tunes, no chatter~
 
""",
"""\
(\\_/)
( •.•) here’s a vibe-filled track~!!
/> Let the music do the talking~
 
""",
"""\
(\\_/)
( •.•) this one’s an instrumental bop~!!
/> Just rhythm and flow~

""",
"""\
(\\_/)
( •.•) pure instrumental joy ahead~!!
/> Words off, beats on~
 
""",
"""\
(\\_/)
( •.•) it’s all melody, no lyrics~!!
/> Vibes so smooth~
 
""",
"""\
(\\_/)
( •.•) tap to the rhythm~!!
/> No words, just feels~
 
""",
"""\
(\\_/)
( •.•) instrumental bliss unlocked~!!
/> Music to move you~
 
""",
"""\
(\\_/)
( •.•) all beats, no chatter~!!
/> Tune in, zone out~
 
""",
"""\
(\\_/)
( •.•) it’s a wordless masterpiece~!!
/> Just the melody to guide you~
 
""",
"""\
(\\_/)
( •.•) immerse in the instrumental~!!
/> No lyrics needed~
 
""",
"""\
(\\_/)
( •.•) word-free and beat-full~!!
/> Dive into the sound~
 
"""
]
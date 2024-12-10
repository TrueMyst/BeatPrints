"""
Module: consts.py

Contains all the necessary co-ordinates that'll
be needed to place the texts/images on the poster.

Prefixes
---------
S = Size
C = Cords
P = Path
CL = Color
"""

import os

MAX_ROWS = 5
MAX_WIDTH = 1020

S_TRACKS = 35
S_SPACING = 45
S_COVER = (1020, 1020)
S_SPOTIFY_CODE = (330, 85)
S_HEADING = 80
S_ARTIST = 60
S_DURATION = 45
S_LYRICS = 42
S_LABEL = 30

C_COVER = (60, 60)
C_HEADING = (60, 1275)
C_ARTIST = (60, 1350)
C_LYRICS = (60, 1395)
C_TRACKS = (60, 1390)
C_LABEL = (1080, 1615)

C_DURATION = (1080, 1275)
C_PALETTE = (60, 1120)
C_ACCENT = (0, 1720, 1140, 1740)
C_SPOTIFY_CODE = (45, 1610)

CL_FONT_DARK_MODE = (193, 189, 178)
CL_FONT_LIGHT_MODE = (50, 47, 48)

CL_WHITE = (255, 255, 255, 255)
CL_TRANSPARENT = (0, 0, 0, 0)

P_FULLPATH = os.path.join(os.path.dirname(__file__))
P_ASSETS = os.path.join(P_FULLPATH, "assets")
P_FONTS = os.path.join(P_ASSETS, "fonts")
P_TEMPLATES = os.path.join(P_ASSETS, "templates")

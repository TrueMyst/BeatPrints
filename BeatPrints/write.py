"""
Module: write.py

Provides modules for image processing and font tools.

Imports:
    - os: Provides OS interaction
    - PIL: Image processing Library
    - fontTools: Font manipulation tools.
    - typing: Type hinting support.
"""

import os
from fontTools.ttLib import TTFont
from PIL import ImageFont, ImageDraw
from typing import Optional, Dict, Literal, Tuple, List


def load_fonts(*font_paths: str) -> Dict[str, TTFont]:
    """
    Loads font files into memory and returns a dictionary of font objects.

    Args:
        *font_paths (str): Paths to the font files.

    Returns:
        Dict[str, TTFont]: Dictionary mapping font names to TTFont objects.
    """
    fonts = {}
    for path in font_paths:
        font = TTFont(path)
        fonts[path] = font
    return fonts


def font(weight: Literal["Regular", "Bold", "Light"]) -> Dict[str, TTFont]:
    """
    Loads fonts of the specified weight from the predefined assets/fonts directory.

    Args:
        weight (Literal["Regular", "Bold", "Light"]): The weight of the fonts to load.

    Returns:
        Dict[str, TTFont]: Dictionary of loaded font objects.
    """
    fonts_path = os.path.realpath(os.path.join("assets", "fonts"))
    font_families = [
        "Oswald", "NotoSansJP", "NotoSansKR", "NotoSansTC", "NotoSansSC",
        "NotoSans"
    ]
    font_paths = [
        os.path.join(fonts_path, family, f"{family}-{weight}.ttf")
        for family in font_families
    ]
    return load_fonts(*font_paths)


def check_glyph(font: TTFont, glyph: str) -> bool:
    """
    Check if a glyph exists in a font.

    Args:
        font (TTFont): Loaded font object.
        glyph (str): Character to check.

    Returns:
        bool: True if the glyph exists, False otherwise.
    """
    try:
        cmap = font.getBestCmap()
        return ord(glyph) in cmap

    except Exception:
        return False


def merge_chunks(text: str, fonts: Dict[str, TTFont]) -> List[List[str]]:
    """
    Merge consecutive characters with the same font into clusters.

    Args:
        text (str): Input text.
        fonts (Dict[str, TTFont]): Dictionary mapping font names to TTFont objects.

    Returns:
        List[List[str]]: Clusters of consecutive characters with the same font.
    """
    chunks = []
    font_path = ""
    universal_chars = ''' ,!@#$%^&*(){}[]+_=-""''?'''
    last_font = next(iter(fonts))

    for char in text:
        char_found = False
        if char in universal_chars:  # Should be rendered by same font
            chunks.append([char, last_font])
            continue

        for font_path, font in fonts.items():
            if check_glyph(font, char):
                last_font = font_path
                char_found = True
                chunks.append([char, font_path])
                break

        if not char_found:
            # If not found, don't skip it
            chunks.append([char, font_path])

    cluster = chunks[:1]

    for char, font_path in chunks[1:]:
        if cluster[-1][1] == font_path:
            cluster[-1][0] += char
        else:
            cluster.append([char, font_path])
    return cluster


def text_v2(draw: ImageDraw.ImageDraw,
            xy: Tuple[int, int],
            text: str,
            color: Tuple[int, int, int],
            fonts: Dict[str, TTFont],
            size: int,
            anchor: Optional[str] = None,
            align: Literal["left", "center", "right"] = "left",
            direction: Literal["rtl", "ltr", "ttb"] = "ltr") -> None:
    """
    Draw text on an image.

    Args:
        draw (ImageDraw.ImageDraw): ImageDraw object.
        xy (Tuple[int, int]): Text coordinates.
        text (str): Text to draw.
        color (Tuple[int, int, int]): RGB color of the text.
        fonts (Dict[str, TTFont]): Dictionary of font names to TTFont objects.
        size (int): Font size.
        anchor (Optional[str], optional): Anchor point for positioning. Defaults to None.
        align (Literal["left", "center", "right"], optional): Text alignment. Defaults to "left".
        direction (Literal["rtl", "ltr", "ttb"], optional): Text direction. Defaults to "ltr".
    """

    x_offset = 0
    sentence = merge_chunks(text, fonts)

    for words in sentence:

        font = ImageFont.truetype(words[1], size)
        box = font.getbbox(words[0])
        xy_ = (xy[0] + x_offset, xy[1])

        draw.text(
            xy=xy_,
            text=words[0],
            fill=color,
            font=font,
            anchor=anchor,
            align=align,
            direction=direction,
            embedded_color=True,
        )
        x_offset += box[2] - box[0]


def multiline_text_v2(draw: ImageDraw.ImageDraw,
                      xy: Tuple[int, int],
                      text: str,
                      color: Tuple[int, int, int],
                      fonts: Dict[str, TTFont],
                      size: int,
                      anchor: Optional[str] = None,
                      spacing: int = 0,
                      align: Literal["left", "center", "right"] = "left",
                      direction: Literal["rtl", "ltr", "ttb"] = "ltr") -> None:
    """
    Draw multiple lines of text on an image.

    Args:
        draw (ImageDraw.ImageDraw): ImageDraw object.
        xy (Tuple[int, int]): Text coordinates.
        text (str): Text to draw.
        color (Tuple[int, int, int]): RGB color of the text.
        fonts (Dict[str, TTFont]): Dictionary of font names to TTFont objects.
        size (int): Font size.
        anchor (Optional[str], optional): Anchor point for positioning. Defaults to None.
        spacing (int, optional): Spacing between lines. Defaults to 0.
        align (Literal["left", "center", "right"], optional): Text alignment. Defaults to "left".
        direction (Literal["rtl", "ltr", "ttb"], optional): Text direction. Defaults to "ltr".
    """

    x, y = xy
    y_offset = 0
    lines = text.split("\n")

    scale = int(round((size * 6) / 42, 1))

    for line in lines:
        xy_ = (x, y + y_offset)
        text_v2(
            draw,
            xy=xy_,
            text=line,
            color=color,
            fonts=fonts,
            size=size,
            anchor=anchor,
            align=align,
            direction=direction,
        )
        y_offset += size + scale + spacing


def heading(draw: ImageDraw.ImageDraw, xy: Tuple[int, int], width_limit: int,
            text: str, color: Tuple[int, int, int], fonts: Dict[str, TTFont],
            size: int) -> None:
    """
    Draw a heading on an image within a specified width limit.

    Args:
        draw (ImageDraw.ImageDraw): ImageDraw object to draw on the image.
        xy (Tuple[int, int]): Coordinates for the heading.
        width_limit (int): Maximum width for the heading.
        text (str): Heading text.
        color (Tuple[int, int, int]): RGB color of the text.
        fonts (Dict[str, TTFont]): Dictionary of font names to TTFont objects.
        size (int): Font size.
    """

    # font_size = 45
    total_length_of_heading = 0
    chunked = merge_chunks(text, fonts)

    while True:
        for word, path in chunked:
            font = ImageFont.truetype(path, size)
            total_length_of_heading += font.getlength(word)

        if total_length_of_heading > width_limit:
            size -= 1
            total_length_of_heading = 0

        elif total_length_of_heading <= width_limit:
            break

    y_offset = 0

    # Draw song name and year
    for words, path in chunked:
        xy_ = (xy[0] + y_offset, xy[1])

        font = ImageFont.truetype(path, size)
        draw.text(
            xy=xy_,
            text=words,
            fill=color,
            font=font,
            anchor="ls",
            embedded_color=True,
        )

        draw.text
        box = font.getbbox(words[0])
        y_offset += box[2] - box[0]

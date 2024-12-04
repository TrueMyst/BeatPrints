"""
Module: write.py

A custom module written to improve Pillow’s draw.text functionality.
"""

import os

from .consts import P_FONTS

from fontTools.ttLib import TTFont
from PIL import ImageFont, ImageDraw
from typing import Optional, Dict, Literal, Tuple, List


def _load_fonts(*font_paths: str) -> Dict[str, TTFont]:
    """
    Loads font files into memory and returns a dictionary of font objects.
    """
    fonts = {}
    for path in font_paths:
        font = TTFont(path)
        fonts[path] = font
    return fonts


def font(weight: Literal["Regular", "Bold", "Light"]) -> Dict[str, TTFont]:
    """
    Loads fonts of the specified weight from the predefined assets/fonts directory.
    """
    fonts_path = P_FONTS
    font_families = [
        "Oswald",
        "NotoSansJP",
        "NotoSansKR",
        "NotoSansTC",
        "NotoSansSC",
        "NotoSans",
    ]
    font_paths = [
        os.path.join(fonts_path, family, f"{family}-{weight}.ttf")
        for family in font_families
    ]
    return _load_fonts(*font_paths)


def _check_glyph(font: TTFont, glyph: str) -> bool:
    """
    Check if a glyph exists in a font.
    """
    try:
        cmap = font.getBestCmap()
        return ord(glyph) in cmap

    except Exception:
        return False


def _merge_chunks(text: str, fonts: Dict[str, TTFont]) -> List[List[str]]:
    """
    Groups consecutive characters with the same font into clusters.
    """
    chunks = []
    font_path = ""
    universal_chars = """ ,!@#$%^&*(){}[]+_=-""''?"""
    last_font = next(iter(fonts))

    for char in text:
        char_found = False
        if char in universal_chars:  # Should be rendered by same font
            chunks.append([char, last_font])
            continue

        for font_path, font in fonts.items():
            if _check_glyph(font, char):
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


def singleline(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    fill: Tuple[int, int, int],
    fonts: Dict[str, TTFont],
    size: int,
    anchor: Optional[str] = None,
    align: Literal["left", "center", "right"] = "left",
    direction: Literal["rtl", "ltr", "ttb"] = "ltr",
) -> None:
    """
    Renders a single line of text at a specified position
    using a chosen font, color, alignment, and text direction.
    """
    x_offset = 0
    sentence = _merge_chunks(text, fonts)

    for char, font_path in sentence:

        font = ImageFont.truetype(font_path, size)
        box = font.getbbox(char)
        xy = (int(xy[0] + x_offset), xy[1])

        draw.text(
            xy=xy,
            text=char,
            fill=fill,
            font=font,
            anchor=anchor,
            align=align,
            direction=direction,
            embedded_color=True,
        )

        x_offset += box[2] - box[0]


def get_length(text: str, fonts: Dict[str, TTFont], size: int) -> int:
    """
    Calculate the width of the text without drawing it.
    """
    total_width = 0
    sentence = _merge_chunks(text, fonts)

    for word, path in sentence:
        font = ImageFont.truetype(path, size)
        total_width += font.getlength(word)  # Add width of character

    return int(total_width)


def text(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    color: Tuple[int, int, int],
    fonts: Dict[str, TTFont],
    size: int,
    anchor: Optional[str] = None,
    spacing: int = 0,
    align: Literal["left", "center", "right"] = "left",
    direction: Literal["rtl", "ltr", "ttb"] = "ltr",
) -> None:
    """
    Renders text on an image at a specified position with
    customizable font, size, color, alignment, direction, and spacing.
    """
    # Choose multiline function if text has line breaks
    if "\n" in text:
        y_offset = 0
        lines = text.split("\n")
        scale = int(round((size * 6) / 42, 1))

        # Call singleline drawing for each line
        for line in lines:
            singleline(
                draw,
                (xy[0], xy[1] + y_offset),
                line,
                color,
                fonts,
                size,
                anchor,
                align,
                direction,
            )
            y_offset += size + scale + spacing
    else:
        # Call singleline drawing for a single line
        singleline(draw, xy, text, color, fonts, size, anchor, align, direction)


def heading(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    width_limit: int,
    text: str,
    color: Tuple[int, int, int],
    fonts: Dict[str, TTFont],
    size: int,
) -> None:
    """
    Draw a heading on an image within a specified width limit.
    """
    total_length_of_heading = 0

    # Pairing words with their respective fonts.
    chunked = _merge_chunks(text, fonts)

    while True:
        for word, path in chunked:
            font = ImageFont.truetype(path, size)
            total_length_of_heading += font.getlength(word)

        # Reduce font size if length exceeds width_limit.
        if total_length_of_heading > width_limit:
            size -= 1
            total_length_of_heading = 0

        elif total_length_of_heading <= width_limit:
            break

    y_offset = 0

    # Track Name or Heading
    for word, path in chunked:
        xy_ = (xy[0] + y_offset, xy[1])

        font = ImageFont.truetype(path, size)
        draw.text(
            xy=xy_,
            text=word,
            fill=color,
            font=font,
            anchor="ls",
            embedded_color=True,
        )

        box = font.getbbox(word)
        y_offset += box[2] - box[0]

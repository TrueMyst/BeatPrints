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


def group_by_font(text: str, fonts: Dict[str, TTFont]) -> List[List[str]]:
    """
    Groups consecutive characters in a string based on the font required to render them.
    """
    groups = []

    # Characters rendered with the default font.
    common_chars = """ ,!@#$%^&*(){}[]+_=-""''?"""

    default_font = next(iter(fonts))
    last_font_path = default_font

    # Assign each character to the correct font.
    for char in text:
        char_matched = False

        # Use the default font for common characters.
        if char in common_chars:
            groups.append([char, last_font_path])
            continue

        # Check which font supports the character.
        for font_path, font in fonts.items():
            if _check_glyph(font, char):
                last_font_path = font_path
                groups.append([char, font_path])
                char_matched = True
                break

        # If no font matches, assign the last used font.
        if not char_matched:
            groups.append([char, last_font_path])

    # Merge consecutive characters with the same font into chunks.
    merged = [groups[0]]
    for char, font_path in groups[1:]:
        if merged[-1][1] == font_path:

            # Append character to the current chunk.
            merged[-1][0] += char
        else:
            merged.append([char, font_path])

    return merged


def render_singleline(
    draw: ImageDraw.ImageDraw,
    pos: Tuple[int, int],
    text: str,
    color: Tuple[int, int, int],
    fonts: Dict[str, TTFont],
    size: int,
    anchor: Optional[str] = None,
    align: Literal["left", "center", "right"] = "left",
    direction: Literal["rtl", "ltr", "ttb"] = "ltr",
) -> None:
    """
    Renders a single line of text on the image with specified styling.
    """
    offset = 0
    formatted_text = group_by_font(text, fonts)

    x, y = pos

    # Render each character
    for char, font_path in formatted_text:
        font = ImageFont.truetype(font_path, size)

        # Get char bounding box
        char_box = font.getbbox(char)

        # Position for char
        char_pos = (x + offset, y)

        draw.text(
            xy=char_pos,
            text=char,
            fill=color,
            font=font,
            anchor=anchor,
            align=align,
            direction=direction,
            embedded_color=True,
        )

        # Update offset for next char
        offset += char_box[2] - char_box[0]


def calculate_text_width(text: str, fonts: Dict[str, TTFont], size: int) -> int:
    """
    Returns the width of the text without drawing it.
    """
    total_width = 0

    # Group text by font
    formatted_text = group_by_font(text, fonts)

    # Sum widths of all words
    for word, path in formatted_text:
        font = ImageFont.truetype(path, size)

        # Add word width
        total_width += font.getlength(word)

    return int(total_width)


def text(
    draw: ImageDraw.ImageDraw,
    pos: Tuple[int, int],
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
    x, y = pos

    # Choose multiline function if text has line breaks
    if "\n" in text:
        y_offset = 0
        lines = text.split("\n")
        scale = int(round((size * 6) / 42, 1))

        # Call render_singleline drawing for each line
        for line in lines:
            render_singleline(
                draw,
                (x, y + y_offset),
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
        # Draw a single line
        render_singleline(draw, pos, text, color, fonts, size, anchor, align, direction)


def heading(
    draw: ImageDraw.ImageDraw,
    pos: Tuple[int, int],
    max_width: int,
    text: str,
    color: Tuple[int, int, int],
    fonts: Dict[str, TTFont],
    size: int,
) -> None:
    """
    Draws a heading within a specified width limit on an image.
    """
    total_width = 0

    # Pair words with corresponding fonts.
    words_fonts = group_by_font(text, fonts)

    # Adjust font size to fit within max_width.
    while True:
        for word, font_path in words_fonts:
            font = ImageFont.truetype(font_path, size)
            total_width += font.getlength(word)

        if total_width > max_width:
            size -= 1  # Reduce font size.
            total_width = 0
        else:
            break

    offset = 0

    # Render each word with its corresponding font.
    for word, font_path in words_fonts:
        word_pos = (pos[0] + offset, pos[1])

        font = ImageFont.truetype(font_path, size)
        draw.text(
            xy=word_pos,
            text=word,
            fill=color,
            font=font,
            anchor="ls",
            embedded_color=True,
        )

        # Update offset based on word width.
        word_width = font.getbbox(word)[2]
        offset += word_width

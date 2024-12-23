"""
Module: write.py

A custom module written to improve Pillow’s draw.text functionality.
"""

import os

from fontTools.ttLib import TTFont
from PIL import ImageFont, ImageDraw
from typing import Optional, Dict, Literal, Tuple, List

from .consts import P_FONTS


def _load_fonts(*font_paths: str) -> Dict[str, TTFont]:
    """
    Loads font files into memory and returns a dictionary of font objects.

    Args:
        *font_paths (str): Paths to font files.

    Returns:
        dict: A dictionary mapping font paths to font objects.
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
        weight (str): The desired font weight ("Regular", "Bold", or "Light").

    Returns:
        dict: A dictionary mapping font paths to font objects for the given weight.
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
    Checks if a specific glyph exists in the given font.

    Args:
        font (TTFont): The font to check.
        glyph (str): The character (glyph) to search for.

    Returns:
        bool: True if the glyph exists in the font, False otherwise.
    """
    try:
        cmap = font.getBestCmap()
        return ord(glyph) in cmap

    except Exception:
        return False


def group_by_font(text: str, fonts: Dict[str, TTFont]) -> List[List[str]]:
    """
    Groups consecutive characters in a string based on the font required to render them.

    Args:
        text (str): The text to be grouped by font.
        fonts (dict): A dictionary mapping font paths to font objects.

    Returns:
        list: A list of lists, where each sublist contains a group of characters
              and their corresponding font path.
    """
    groups = []

    # Common characters to render with the default font.
    common_chars = """ ,!@#$%^&*(){}[]+_=-""''?"""

    # Use the first font in the dictionary as the default font.
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

    # Merge consecutive characters that use the same font into one group.
    merged = [groups[0]]
    for char, font_path in groups[1:]:

        # Append the character to the current group.
        if merged[-1][1] == font_path:
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
) -> None:
    """
    Renders a single line of text on the image with specified styling.

    Args:
        draw (ImageDraw.ImageDraw): The drawing context.
        pos (tuple): The (x, y) position to start drawing.
        text (str): The text to render.
        color (tuple): The text color in RGB format.
        fonts (dict): A dictionary of fonts to use.
        size (int): The font size.
        anchor (str, optional): Text anchor for alignment.
        align (str, optional): Text alignment ("left", "center", "right").
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
            embedded_color=True,
        )

        # Update offset for next char
        offset += char_box[2] - char_box[0]


def calculate_text_width(text: str, fonts: Dict[str, TTFont], size: int) -> int:
    """
    Returns the width of the text without drawing it.

    Args:
        text (str): The text to measure.
        fonts (dict): A dictionary of fonts to use.
        size (int): The font size.

    Returns:
        int: The width of the text.
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
) -> None:
    """
    Renders text on an image at a specified position with customizable font, size, color, alignment, and spacing.

    Args:
        draw (ImageDraw.ImageDraw): The drawing context.
        pos (tuple): The (x, y) position to start drawing.
        text (str): The text to render.
        color (tuple): The text color in RGB format.
        fonts (dict): A dictionary of fonts to use.
        size (int): The font size.
        anchor (str, optional): Text anchor for alignment.
        spacing (int, optional): Vertical spacing between lines.
        align (str, optional): Text alignment ("left", "center", "right").
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
                draw, (x, y + y_offset), line, color, fonts, size, anchor, align
            )
            y_offset += size + scale + spacing
    else:
        # Draw a single line
        render_singleline(draw, pos, text, color, fonts, size, anchor, align)


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

    Args:
        draw (ImageDraw.ImageDraw): The drawing context.
        pos (tuple): The (x, y) position to start drawing.
        max_width (int): The maximum width allowed for the heading.
        text (str): The text to render.
        color (tuple): The text color in RGB format.
        fonts (dict): A dictionary of fonts to use.
        size (int): The font size.
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

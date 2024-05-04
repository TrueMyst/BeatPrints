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


def check_glyph(font: TTFont, glyph: str) -> bool:
    """
    Check if a glyph exists in a font.

    Args:
        font_file (str): Path to the font file.
        char (str): Character to check.

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
    Merge consecutive characters with the same font into clusters for optimized font lookup.

    Args:
        text (str): The input text to be processed.
        fonts (Dict[str, TTFont]): A dictionary mapping font names to TTFont objects.

    Returns:
        List[List[str]]: A list of clusters where each cluster contains consecutive characters with the same font.
    """
    chunks = []

    for char in text:
        for font_path, font in fonts.items():
            if check_glyph(font, char):
                chunks.append([char, font_path])
                break

    cluster = chunks[:1]

    for char, font_path in chunks[1:]:
        if cluster[-1][1] == font_path:
            cluster[-1][0] += char
        else:
            cluster.append([char, font_path])

    return cluster


def draw_text_v2(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    color: Tuple[int, int, int],
    fonts: Dict[str, TTFont],
    size: int,
    anchor: Optional[str] = None,
    align: Literal["left", "center", "right"] = "left",
    direction: Literal["rtl", "ltr", "ttb"] = "ltr",
) -> None:
    """
    Draws text on an image.

    Args:
        draw (ImageDraw.ImageDraw): The ImageDraw object.
        xy (Tuple[int, int]): The xy coordinates for the text.
        text (str): The text to be drawn.
        color (Tuple[int, int, int]): The RGB color of the text.
        fonts (Dict[str, TTFont]): A dictionary of font names to TTFont objects.
        size (int): The font size.
        anchor (Optional[str], optional): The anchor point for positioning the text. Defaults to None.
        align (Literal["left", "center", "right"], optional): The alignment of the text. Defaults to "left".
        direction (Literal["rtl", "ltr", "ttb"], optional): The direction of the text. Defaults to "ltr".
    """

    y_offset = 0
    sentence = merge_chunks(text, fonts)

    for words in sentence:
        cords = (xy[0] + y_offset, xy[1])

        font = ImageFont.truetype(words[1], size)
        draw.text(
            xy=cords,
            text=words[0],
            fill=color,
            font=font,
            anchor=anchor,
            align=align,
            direction=direction,
            embedded_color=True,
        )

        draw.text
        box = font.getbbox(words[0])
        y_offset += box[2] - box[0]


def draw_multiline_text_v2(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    color: Tuple[int, int, int],
    fonts: Dict[str, TTFont],
    size: int,
    anchor: Optional[str] = None,
    align: Literal["left", "center", "right"] = "left",
    direction: Literal["rtl", "ltr", "ttb"] = "ltr",
) -> None:
    """
    Draws multiple lines of text on an image, handling newline characters and adjusting spacing between lines.
    """
    spacing = xy[1]
    lines = text.split("\n")

    for line in lines:
        mod_cord = (xy[0], spacing)
        draw_text_v2(
            draw,
            xy=mod_cord,
            text=line,
            color=color,
            fonts=fonts,
            size=size,
            anchor=anchor,
            align=align,
            direction=direction,
        )
        spacing += size + 5


def heading(
    draw: ImageDraw.ImageDraw,
    xy: tuple,
    width_limit: int,
    text: str,
    color: tuple,
    fonts: Dict[str, TTFont],
):
    """
    A custom made function that draws a title consisting of a song name and year on the image.

    Args:
        draw (ImageDraw.ImageDraw): An ImageDraw object to draw on the image.
        textbox (tuple): Cordinates defining the bounding box for the title.
        name (str): The song name.
        year (str): The release year of the song.
        font (str): The path to the font file.
        initial_size (int): The initial font size.
    """

    font_size = 35
    total_length_of_heading = 0
    chunked = merge_chunks(text, fonts)

    while True:
        for word, path in chunked:
            font = ImageFont.truetype(path, font_size)
            total_length_of_heading += font.getlength(word)

        if total_length_of_heading > width_limit:
            font_size -= 1
            total_length_of_heading = 0

        elif total_length_of_heading <= width_limit:
            break

    y_offset = 0

    # Draw song name and year
    for words, path in chunked:
        xy_ = (xy[0] + y_offset, xy[1])

        font = ImageFont.truetype(path, font_size)
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

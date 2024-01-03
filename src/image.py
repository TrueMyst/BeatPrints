from color import palette
from PIL import Image, ImageDraw, ImageFont
import pathlib

def draw_palette(draw: ImageDraw.ImageDraw, path: str, accent: bool):
    for i in range(6):
        start, end = 85 * i, 85 * (i + 1)
        draw.rectangle(((30 + start, 560), (30 + end, 580)), fill=palette(path)[i])

    if accent == True:
        draw.rectangle(((0, 860), (570, 870)), fill=sorted(palette(path))[-2])


def replace_pixels(path):
    with Image.open(path) as img:
        img = img.convert("RGBA")
        pixels = img.load()

        white = (255, 255, 255, 255)
        transparent = (0, 0, 0, 0)

        width, height = img.size

        for x in range(width):
            for y in range(height):
                pixels[x, y] = (
                    transparent if pixels[x, y] != white else (50, 47, 48, 255)
                )
        cur = pathlib.Path(__file__).parent.resolve()
        img.save(cur / "assets/spotify_code.png")


def write_text(draw: ImageDraw.ImageDraw, cords, text, font, size, anchor="lt"):
    font_ = ImageFont.truetype(font, size)
    draw.text(
        xy=(cords[0], cords[1]), text=text, fill=(50, 47, 48), font=font_, anchor=anchor
    )


def write_multiline_text(draw: ImageDraw.ImageDraw, cords, text: str, font, size):
    font_ = ImageFont.truetype(font, size)
    draw.text(
        xy=(cords[0], cords[1]), text=text, fill=(50, 47, 48), font=font_, spacing=0
    )


def write_title(
    draw: ImageDraw.ImageDraw,
    textbox: tuple,
    name,
    year,
    font,
    initial_size,
):
    length = textbox[2] - textbox[0]
    size = initial_size

    while True:
        font_ = ImageFont.truetype(font, size)
        _, _, text_width, _ = draw.textbbox((textbox[0], textbox[1]), name, font=font_)

        if text_width <= length or size <= 1:
            break
        size -= 1

    year_font = ImageFont.truetype(font, 20)

    name_textbox = draw.textbbox(
        (textbox[0], textbox[1]), name, font=font_, anchor="lt"
    )
    year_getbox = year_font.getbbox(year)

    width_for_year = name_textbox[2] + 10
    height_for_year = textbox[3] - (year_getbox[3] - year_getbox[1])

    diff = textbox[3] - name_textbox[3]
    width_for_name = textbox[0]
    height_for_name = textbox[1] + diff

    write_text(draw, (width_for_name, height_for_name), name, font, size)
    write_text(draw, (width_for_year, height_for_year), year, font, 20)

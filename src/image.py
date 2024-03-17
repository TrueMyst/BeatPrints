import pathlib
from color import palette
from PIL import Image, ImageDraw, ImageFont

cur = pathlib.Path(__file__).parent.resolve()


def draw_palette(draw: ImageDraw.ImageDraw, image_path: str, accent: bool):
    """
    Calculates the coordinates of the color palette to be drawn.
    """
    for i in range(6):
        start, end = 85 * i, 85 * (i + 1)
        draw.rectangle(
            ((30 + start, 560), (30 + end, 580)), fill=palette(image_path)[i]
        )

    if accent:
        draw.rectangle(((0, 860), (570, 870)), fill=palette(image_path)[-1])


def crop_to_square(image_path: str, save_path: str):
    """
    Crops any given image into 1:1 ratio and saves it.
    """
    image = Image.open(image_path)

    def chop(image):
        width, height = image.size
        min_dimension = min(width, height)
        left = (width - min_dimension) / 2
        top = (height - min_dimension) / 2
        right = (width + min_dimension) / 2
        bottom = (height + min_dimension) / 2
        return image.crop((left, top, right, bottom))

    # Crop the image to a 1:1 ratio and save it
    cropped_image = chop(image)
    cropped_image.save(save_path)


def remove_white_pixel(image_path: str):
    """
    A custom function that removes white pixels from the background and makes it transparent.
    """
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        pixels = img.load()

        transparent = (0, 0, 0, 0)
        white = (255, 255, 255, 255)

        width, height = img.size

        for x in range(width):
            for y in range(height):
                pixels[x, y] = (
                    transparent if pixels[x, y] != white else (50, 47, 48, 255)
                )

        img.save(cur / "assets/spotify_code.png")


def write_text(
    draw: ImageDraw.ImageDraw,
    cords: tuple,
    text: str,
    font: str,
    size: int,
    anchor="lt",
):
    """
    A custom function that lets you draw single-line text with easy customizability
    """
    font = ImageFont.truetype(font, size)
    draw.text(
        xy=(cords[0], cords[1]), text=text, fill=(50, 47, 48), font=font, anchor=anchor
    )


def write_multiline_text(
    draw: ImageDraw.ImageDraw, cords: tuple, text: str, font: str, size: int
):
    """
    A custom function that lets you draw multi-line text with easy customizability
    """
    font = ImageFont.truetype(font, size)
    draw.multiline_text(
        xy=(cords[0], cords[1]), text=text, fill=(50, 47, 48), font=font, spacing=0
    )


def write_title(
    draw: ImageDraw.ImageDraw,
    textbox: tuple,
    name: str,
    year: str,
    font: str,
    initial_size: int,
):
    size = initial_size
    length = textbox[2] - textbox[0]

    while True:
        title_font = ImageFont.truetype(font, size)
        _, _, text_width, _ = draw.textbbox(
            (textbox[0], textbox[1]), name, font=title_font
        )

        if text_width <= length or size <= 1:
            break
        size -= 1

    year_font = ImageFont.truetype(font, 20)

    name_textbox = draw.textbbox(
        (textbox[0], textbox[1]), name, font=title_font, anchor="lt"
    )
    year_getbox = year_font.getbbox(year)

    # This is the height that is used to adjust the song name
    extra_height = textbox[3] - name_textbox[3]

    # The space between the name and the year (currently 7)
    year_x = name_textbox[2] + 7
    year_y = textbox[3] - (year_getbox[3] - year_getbox[1])

    name_x = textbox[0]
    name_y = textbox[1] + extra_height

    write_text(draw, (name_x, name_y), name, font, size)
    write_text(draw, (year_x, year_y), year, font, 20)

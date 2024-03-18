"""
Module: image.py

Dependicies:
    1. PIL: Image Processing
    2. color: Extract color palette
"""
import pathlib
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import color

# Get the current dictionary path
path_to_current_dictionary = pathlib.Path(__file__).parent.resolve()

def draw_palette(
        draw: ImageDraw.ImageDraw,
        image_path: str,
        accent: bool
        ):

    """
    Draws the color palette on the image.
    
    Args:
        draw (ImageDraw.ImageDraw): An ImageDraw object to draw on the image.
        image_path (str): The path of the image file.
        accent (bool): Flag indicating whether to highlight the accent color.
    """

    # Get the color palette from the image
    color_palette = color.get_color_palette(image_path)

    # Draw rectangles for each color in the palette
    for i in range(6):
        start, end = 85 * i, 85 * (i + 1)
        draw.rectangle(
            ((30 + start, 560), (30 + end, 580)), fill=color_palette[i]
        )

    # Optionally draw a rectangle to highlight the accent color
    if accent:
        draw.rectangle(((0, 860), (570, 870)), fill=color_palette[-1])


def crop_to_square(
        image_path: str,
        save_path: str
        ):

    """
    Crops the image to a square aspect ratio and saves it.
    
    Args:
        image_path (str): The path of the original image file.
        save_path (str): The path where the cropped image will be saved.
    """

    # Open the image
    image = Image.open(image_path)

    # Function to crop the image to a square aspect ratio
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


def remove_white_pixel(
        image_path: str
        ):

    """
    Removes white pixels from the image background and makes them transparent.
    
    Args:
        image_path (str): The path of the image file.
    """

    # Open the image as img
    with Image.open(image_path) as img:

        # Convert the image into RGBA mode
        img = img.convert("RGBA")
        pixels = img.load()

        # Define colors
        transparent = (0, 0, 0, 0)
        white = (255, 255, 255, 255)

        width, height = img.size

        # Iterate through pixels and make white pixels transparent
        for x in range(width):
            for y in range(height):
                pixels[x, y] = (
                    transparent if pixels[x, y] != white else (50, 47, 48, 255)
                )

        # Save the modified image
        img.save(path_to_current_dictionary / "assets/spotify_code.png")


def write_text(
    draw: ImageDraw.ImageDraw,
    cords: tuple,
    text: str,
    font: str,
    size: int,
    anchor="lt",
    ):

    """
    Draws single-line text on the image.
    
    Args:
        draw (ImageDraw.ImageDraw): An ImageDraw object to draw on the image.
        cords (tuple): Coordinates (x, y) where the text will be drawn.
        text (str): The text to be drawn.
        font (str): The path to the font file.
        size (int): The font size.
        anchor (str, optional): The anchor point for text alignment. Defaults to "lt" (left-top).
    """

    # Load the font
    font = ImageFont.truetype(font, size)

    # Draw the text
    draw.text(
        xy=(cords[0], cords[1]), text=text, fill=(50, 47, 48), font=font, anchor=anchor
    )


def write_multiline_text(
    draw: ImageDraw.ImageDraw,
    cords: tuple,
    text: str,
    font: str,
    size: int
    ):

    """
    Draws multi-line text on the image.
    
    Args:
        draw (ImageDraw.ImageDraw): An ImageDraw object to draw on the image.
        cords (tuple): Coordinates (x, y) where the text will be drawn.
        text (str): The text to be drawn.
        font (str): The path to the font file.
        size (int): The font size.
    """

    # Load the font
    font = ImageFont.truetype(font, size)

    # Draw the multi-line text
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

    """
    Draws a title consisting of a song name and year on the image.
    
    Args:
        draw (ImageDraw.ImageDraw): An ImageDraw object to draw on the image.
        textbox (tuple): Coordinates (x1, y1, x2, y2) defining the bounding box for the title.
        name (str): The song name.
        year (str): The release year of the song.
        font (str): The path to the font file.
        initial_size (int): The initial font size.
    """

    size = initial_size
    length = textbox[2] - textbox[0]

    # Adjust font size to fit the title within the textbox width
    while True:
        title_font = ImageFont.truetype(font, size)
        _, _, text_width, _ = draw.textbbox(
            (textbox[0], textbox[1]), name, font=title_font
        )

        if text_width <= length or size <= 1:
            break
        size -= 1

    # Load font for year
    year_font = ImageFont.truetype(font, 20)

    # Get bounding box for name and year
    name_textbox = draw.textbbox(
        (textbox[0], textbox[1]), name, font=title_font, anchor="lt"
    )
    year_getbox = year_font.getbbox(year)

    #Calculate adjustments for positioning

    # This is the height that is used to adjust the song name
    extra_height = textbox[3] - name_textbox[3]

    # The space between the name and the year (currently 7)
    year_x = name_textbox[2] + 7
    year_y = textbox[3] - (year_getbox[3] - year_getbox[1])

    name_x = textbox[0]
    name_y = textbox[1] + extra_height

    # Draw song name and year
    write_text(draw, (name_x, name_y), name, font, size)
    write_text(draw, (year_x, year_y), year, font, 20)

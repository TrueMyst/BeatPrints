import lyrics
import spotify
import utils

from image import *
from PIL import Image, ImageDraw

want_custom_image = utils.confirm_input(
    "[🌃] Do you want to include a custom image as the cover of the posters?"
)
want_accent = utils.confirm_input(
    "[🤌] Would you like to add a stylish color accent at the bottom of your poster?"
)
search = spotify.search_track(
    input("[🍀] you know what you've to do: "), want_custom_image
)

path = search["path"]
id = search["track_id"]
name = search["name"].upper()
year = search["year"].split("-")[0]
artist = search["artist"]
duration = search["duration"]
label = spotify.label(search["album_id"])

lyrics = lyrics.get_extract(search["name"], search["artist"])
color = (50, 47, 48)

gen_code = spotify.get_code(id)

with Image.open(path) as banner:
    banner = banner.resize((510, 510))

with Image.open("./assets/spotify_code.png") as spotify_code:
    spotify_code = spotify_code.resize((150, 38)).convert("RGBA")

with Image.open("./assets/banner_v1.png") as poster:
    poster.paste(banner, (30, 30))
    poster.paste(spotify_code, (20, 807), spotify_code)

    draw = ImageDraw.Draw(poster)
    draw_palette(draw, path, want_accent)

    write_title(
        draw, (30, 602, 437, 637), name, year, "../fonts/Oswald/Oswald-Bold.ttf", 40
    )

    write_text(draw, (30, 649), artist, "../fonts/Oswald/Oswald-Regular.ttf", 30)
    write_text(draw, (496, 616), duration, "../fonts/Oswald/Oswald-Regular.ttf", 20)

    write_multiline_text(
        draw, (30, 685), lyrics, "../fonts/Oswald/Oswald-Light.ttf", 21
    )

    write_text(
        draw,
        (545, 810),
        label[0],
        "../fonts/Oswald/Oswald-Regular.ttf",
        13,
        anchor="rt",
    )
    write_text(
        draw,
        (545, 825),
        label[1],
        "../fonts/Oswald/Oswald-Regular.ttf",
        13,
        anchor="rt",
    )

    utils.create_folder()
    filename = f"{utils.create_filename(name, artist)}_{utils.special_code()}"

    poster.save(f"../images/{filename}.png")

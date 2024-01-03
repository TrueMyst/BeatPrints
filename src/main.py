import lyrics
import spotify
import utils
import pathlib

from image import *
from PIL import Image, ImageDraw

cur = pathlib.Path(__file__).parent.resolve()

want_custom_image = utils.confirm_input(
    "[🌃] Do you want to include a custom image as the cover of the posters?"
)
want_accent = utils.confirm_input(
    "[🤌] Would you like to add a stylish color accent at the bottom of your poster?"
)
search = spotify.search_track(
    input("[🍀] Enter song to search: "), want_custom_image
)

path =  cur  / search["path"]
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

with Image.open(cur / "assets/spotify_code.png") as spotify_code:
    spotify_code = spotify_code.resize((150, 38)).convert("RGBA")

with Image.open(cur / "assets/banner_v1.png") as poster:
    poster.paste(banner, (30, 30))
    poster.paste(spotify_code, (20, 807), spotify_code)
    font = pathlib.Path.resolve( cur / "../fonts/Oswald/")
    font_regular = font / "Oswald-Regular.ttf"
    font_bold = font / "Oswald-Bold.ttf"
    font_light = font / "Oswald-Light.ttf"
    
    draw = ImageDraw.Draw(poster)
    draw_palette(draw, path, want_accent)

    write_title(
        draw, (30, 602, 437, 637), name, year, str(font_bold), 40
    )

    write_text(draw, (30, 649), artist, str(font_regular), 30)
    write_text(draw, (496, 616), duration, str(font_regular), 20)

    write_multiline_text(
        draw, (30, 685), lyrics, str(font_light), 21
    )

    write_text(
        draw,
        (545, 810),
        label[0],
        str(font_regular),
        13,
        anchor="rt",
    )
    write_text(
        draw,
        (545, 825),
        label[1],
        str(font_regular),
        13,
        anchor="rt",
    )

    utils.create_folder()
    filename = f"{utils.create_filename(name, artist)}_{utils.special_code()}"

    out = cur / f"../images/{filename}.png"
    poster.save(out)
    print(f"Image save to {out}")

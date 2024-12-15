import os
import toml
import platform
import questionary

from rich import print
from cli import exutils, validate
from BeatPrints import lyrics, spotify, poster, errors

# Determine the config path based on the platform
config_dir = (
    os.getenv("APPDATA")
    if platform.system() == "Windows"
    else os.path.expanduser("~/.config")
)
config_path = os.path.join(str(config_dir), "BeatPrints", "config.toml")

with open(config_path) as config:
    config = toml.load(config)

POSTERS_DIR = config["general"]["output_directory"]
SEARCH_LIMIT = config["general"]["search_limit"]
CLIENT_ID = config["credentials"]["client_id"]
CLIENT_SECRET = config["credentials"]["client_secret"]


# Initialize the instances
def initialize():
    return (
        lyrics.Lyrics(),
        poster.Poster(POSTERS_DIR),
        spotify.Spotify(CLIENT_ID, CLIENT_SECRET),
    )


ly, ps, sp = initialize()


def select_item(item, limit):
    repeat = True
    query, result = "", []
    emoji, get, table = "", None, None

    # Set emoji, get method, and table method based on the item
    if item == "track":
        emoji = "🎺"
        get = sp.get_track
        table = exutils.tablize_track

    elif item == "album":
        emoji = "💿️"
        get = sp.get_album
        table = exutils.tablize_albums

    prompt = f"{emoji} • Type out the {item} you love the most:"

    while repeat:
        # Prompt the user for input
        query = questionary.text(prompt, style=exutils.default).ask()

        if get:
            result = get(query, limit=limit)

        exutils.clear()

        # Display the results in a table
        print(f'{len(result)} results found for "{query}"!')
        if table:
            print(table(result))

        # Ask if the user wants to search again
        repeat = questionary.confirm(
            "🥞 • Not what you wanted? Want to search again?",
            default=True,
            style=exutils.default,
        ).ask()

        if not repeat:
            # Let the user select their preferred track or album
            choice = questionary.text(
                f"🍀 • Select the {item} you like:",
                validate=validate.NumericValidator(limit=len(result)),
                style=exutils.default,
            ).ask()

            # Clear Screen and return the selected choice
            exutils.clear()
            return result[int(choice) - 1]


def handle_lyrics(ly, track):
    try:
        # Fetch lyrics for the selected track
        lyrics_result = ly.get_lyrics(track)
        print(exutils.format_lyrics(track.name, track.artist, lyrics_result))

        # Let the user select any 4 lines from the lyrics
        range_ = questionary.text(
            "🎀 • Select any 4 of your favorite lines (e.g., 2-5, 7-10):",
            validate=validate.SelectionValidator(lyrics_result),
            style=exutils.default,
        ).ask()

        # Return the highlighted lyrics
        return ly.select_lines(lyrics_result, range_)

    except errors.NoLyricsAvailable:
        print("\n😦 • Couldn't find lyrics from sources.")

        # Handle case when no lyrics are found
        return questionary.text(
            "🎀 • Paste your lyrics below:",
            validate=validate.LineCountValidator,
            style=exutils.default,
        ).ask()


def create_poster():
    try:
        # Ask for the poster type (Song or Album)
        poster_type = questionary.select(
            "🎨 • What type of poster would you like to create?",
            choices=["Song Poster", "Album Poster"],
            style=exutils.default,
        ).ask()

        # Ask for poster features
        features = questionary.form(
            theme=questionary.confirm(
                "💫 • Enable dark mode?", default=False, style=exutils.default
            ),
            accent=questionary.confirm(
                "🌈 • Add a color accent?", default=False, style=exutils.default
            ),
            cimage=questionary.confirm(
                "🥞 • Use a custom image?", default=False, style=exutils.default
            ),
        ).ask()

        # Ask for custom image if required
        image = (
            questionary.path(
                "╰─ 🍞 • Provide the file path to the image:",
                validate=validate.ImagePathValidator,
                style=exutils.default,
            )
            .skip_if(not features["cimage"], default=None)
            .ask()
        )

        # Clear Screen before proceeding
        exutils.clear()

        if poster_type == "Song Poster":
            track = select_item("track", SEARCH_LIMIT)

            if track:
                lyrics = handle_lyrics(ly, track)
                ps.track(track, lyrics, features["accent"], features["theme"], image)

        else:
            index = questionary.confirm(
                "🍙 • Number the tracks?", style=exutils.default
            ).ask()

            album = select_item("album", SEARCH_LIMIT)

            if album:
                ps.album(album, index, features["accent"], features["theme"], image)

    except Exception:
        return "🤚 Exiting..."


def main():
    exutils.clear()
    create_poster()

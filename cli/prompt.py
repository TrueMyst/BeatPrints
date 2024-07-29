# ---------------------------------------------------
# This snippet below is intended for addressing
# import issues and testing purposes. Please refrain
# from including it in your final script.
# ---------------------------------------------------
import os, sys

sys.path.append(os.path.join(os.pardir, "BeatPrints"))
# ---------------------------------------------------

import exutils, validate
import dotenv, questionary
import lyrics, spotify, poster, errors

from rich import print

dotenv.load_dotenv()

# Retrieve Spotify API credentials from environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Initialize classes and variables
SPOTIFY_SONG_LIMIT = 7
ly = lyrics.Lyrics()
ps = poster.Poster()
sp = spotify.Spotify(str(CLIENT_ID), str(CLIENT_SECRET))

# Clear the screen and print the initial banner
exutils.clear()

# Prompt the user for poster features
features = questionary.form(
    theme=questionary.confirm(
        "💫 • Would you like a dark mode for your poster?",
        default=False,
        style=exutils.default,
    ),
    accent=questionary.confirm(
        "🌈 • Add a stylish color accent at the bottom?",
        default=False,
        style=exutils.default,
    ),
    cimage=questionary.confirm(
        "🥞 • Use a custom image as the cover of your poster?",
        default=False,
        style=exutils.default,
    ),
).ask()


image = (
    questionary.path(
        "╰─ 🍞 • Awesome, please provide the file path to the image:",
        validate=validate.ImagePathValidator,
        style=exutils.default,
    )
    .skip_if(not features["cimage"], default=None)
    .ask()
)

# Clear the screen and print the banner again
exutils.clear()

# Prompt the user for their favorite song until a valid result is found
query, tracks = "", []
while not tracks:
    query = questionary.text(
        "🎺 • Type out the song you love the most:", style=exutils.default
    ).ask()
    tracks = sp.search(query, limit=SPOTIFY_SONG_LIMIT)
    if not tracks:
        print("╰─ 😔 • I couldn't find the song, try again")

# Clear the screen and print the banner again
exutils.clear()

# Print the list of songs in a pretty table
print(f'{len(tracks)} results were found for "{query}"!')
print(exutils.tablize(tracks))

# Prompt the user to select a song from the list
choice = questionary.text(
    "🍀 • Select the one you like:",
    validate=validate.NumericValidator(limit=SPOTIFY_SONG_LIMIT),
    style=exutils.default,
).ask()

# Clear the screen and print the banner again
exutils.clear()

# Get track information and lyrics
track = tracks[int(choice) - 1]

try:
    lyrics_result = ly.get_lyrics(track["name"], track["artist"])
    formatted_lyrics = exutils.format_lyrics(
        track["name"], track["artist"], lyrics_result
    )
    print(formatted_lyrics)

    # Prompt the user for the range of the lyrics to select
    range_ = questionary.text(
        "🎀 • Select any 4 of your favorite lines from here (eg: 2-5, 7-10):",
        validate=validate.SelectionValidator(lyrics_result),
        style=exutils.default,
    ).ask()

    lyrics_ = ly.select_lines(lyrics_result, range_)
except errors.NoLyricsAvailable:
    print("\n😦 • Unfortunately, I couldn't find the lyrics from my sources")
    print("📝 • But don't worry, you can paste the lyrics manually below:\n")

    lines = [input(f"Line {i + 1}: ") for i in range(4)]
    lyrics_ = "\n".join(lines)

# Clear the screen and print the banner again
exutils.clear()

# Generate the poster with the selected features and lyrics
ps.generate(track, lyrics_, features["accent"], features["theme"], image)

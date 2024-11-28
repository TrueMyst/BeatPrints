import os
import requests

import exutils, validate
import dotenv, questionary

from rich import print
from BeatPrints import lyrics, spotify, poster, errors

dotenv.load_dotenv()

# Create posters directory if it doesn't exist
POSTERS_DIR = os.path.join(os.path.dirname(__file__), "..", "posters")
os.makedirs(POSTERS_DIR, exist_ok=True)

# Retrieve Spotify API credentials from environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Initialize classes and variables
SPOTIFY_SONG_LIMIT = 7
ly = lyrics.Lyrics()
ps = poster.Poster(POSTERS_DIR)
sp = spotify.Spotify(str(CLIENT_ID), str(CLIENT_SECRET))

# Clear the screen and print the initial banner
exutils.clear()

# Ask user if they want to create a song or album poster
poster_type = questionary.select(
    "🎨 • What type of poster would you like to create?",
    choices=["Song Poster", "Album Poster"],
    style=exutils.default
).ask()

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

if poster_type == "Song Poster":
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
        lyrics_result = ly.get_lyrics(track)
        formatted_lyrics = exutils.format_lyrics(track.name, track.artist, lyrics_result)

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

        lyrics_ = questionary.text(
            "🎀 • But don't worry, you can paste your lyrics down below: \n",
            validate=validate.LineCountValidator,
            style=exutils.default,
        ).ask()

    # Clear the screen and print the banner again
    exutils.clear()

    # Generate the poster with the selected features and lyrics
    ps.generate(track, lyrics_, features["accent"], features["theme"], image)

else:  # Album Poster
    # Prompt the user for their favorite album until a valid result is found
    query, albums = "", []
    while not albums:
        query = questionary.text(
            "💿 • Type out the album you love the most:", style=exutils.default
        ).ask()
        
        # Search for albums
        params = {"q": query, "type": "album", "limit": SPOTIFY_SONG_LIMIT}
        search_response = requests.get(
            f"{sp._Spotify__BASE_URL}/search", 
            params=params, 
            headers=sp._Spotify__AUTH_HEADER
        ).json()
        
        albums = search_response.get("albums", {}).get("items", [])
        if not albums:
            print("╰─ 😔 • I couldn't find the album, try again")

    # Clear the screen and print the banner again
    exutils.clear()

    # Print the list of albums
    print(f'{len(albums)} results were found for "{query}"!')
    
    # Create and print album table
    table = exutils.tablize_albums(albums)
    print(table)

    # Prompt user to select an album
    choice = questionary.text(
        "🍀 • Select the one you like:",
        validate=validate.NumericValidator(limit=len(albums)),
        style=exutils.default,
    ).ask()

    # Clear the screen and print the banner again
    exutils.clear()

    # Get album metadata
    album_id = albums[int(choice) - 1]["id"]
    album_metadata = sp.get_album(album_id)

    # Generate the album poster
    ps.generate_album(album_metadata, features["accent"], features["theme"], image)

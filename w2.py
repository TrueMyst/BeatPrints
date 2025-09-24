import os
from BeatPrints import lyrics, poster, spotify
from BeatPrints import TrackMetadata

# Spotify credentials
CLIENT_ID = SPOTIFY_CLIENT_ID = "5dda5144c6d041e380261738bd36eeae"
CLIENT_SECRET = SPOTIFY_CLIENT_SECRET = "5ed80e0cf7fa4808852fbbe9474752a6"

ly = lyrics.Lyrics()
ps = poster.Poster("./")
sp = spotify.Spotify(CLIENT_ID, CLIENT_SECRET)

# Search for the track and fetch metadata
search = sp.get_track("sorry, i like you too - burbank", limit=1)

# Pick the first result
metadata = search[0]

# Get lyrics for the track
lyrics = ly.get_lyrics(metadata)

simplelyric = """
I'm feeling jazzed up when you text me back
Even though it's been a day
And you probably saw it
"""

# Use the placeholder for instrumental tracks; otherwise, select specific lines
highlighted_lyrics = (
    lyrics if ly.check_instrumental(metadata) else ly.select_lines(lyrics, "2-4")
)

highlighted_lyrics = lyrics(simplelyric)

# Generate the track poster
ps.track(metadata, highlighted_lyrics, theme="Light", a4=True)
import os
from BeatPrints import lyrics, poster, spotify
from BeatPrints import TrackMetadata

# Spotify credentials
CLIENT_ID = SPOTIFY_CLIENT_ID = "5dda5144c6d041e380261738bd36eeae"
CLIENT_SECRET = SPOTIFY_CLIENT_SECRET = "5ed80e0cf7fa4808852fbbe9474752a6"

# 
# Initialize components
ps = poster.Poster("./")
sp = spotify.Spotify(CLIENT_ID, CLIENT_SECRET)

# Search for an album
search = sp.get_album("lose myself - starfall", limit=1)

# Get the album's metadata
metadata = search[0]

# Generate the album poster
ps.album(metadata, indexing=True, a4=True)  # A4 2480×3508 (printable)
import os
import toml
import platform
from rich import print

# Determine the config directory path based on the platform
config_dir = (
    os.getenv("APPDATA")
    if platform.system() == "Windows"
    else os.path.expanduser("~/.config")
)

# Set the full path to the BeatPrints configuration file
config_path = os.path.join(str(config_dir), "BeatPrints", "config.toml")

# Attempt to load the configuration file
try:
    with open(config_path) as config:
        config = toml.load(config)

    # Grab the configuration needed
    POSTERS_DIR = config["general"]["output_directory"]
    SEARCH_LIMIT = config["general"]["search_limit"]

    # if the user chooses not to use Spotify's API
    CLIENT_ID = config.get("credentials").get("client_id")
    CLIENT_SECRET = config.get("credentials").get("client_secret")

except FileNotFoundError:
    print("The config file for BeatPrints doesn't exist. Please create one properly.")
    exit(1)

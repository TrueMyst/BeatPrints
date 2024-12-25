import os
import toml
import platform

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

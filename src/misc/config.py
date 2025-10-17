#! python3

# Global Configuration Module.

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

# --- Path to configuration file ---
ENV_VARIABLES_PATH = PROJECT_ROOT / "assets" / "data" / "env_variables.json"

def load_config(path: Path) -> dict:
    """Loads and parses the JSON configuration file."""
    with open(path, "r") as json_file:
        return json.load(json_file)

# Load the configuration. This code runs only once when the module is imported.
CONFIG = load_config(ENV_VARIABLES_PATH)

# --- Define critical application paths centrally ---
DB_FILE_PATH = PROJECT_ROOT / "assets" / "data" / "sqlite3_data_file.db"
TITLE_ART_PATH = PROJECT_ROOT / "assets" / "art" / "title_art.txt"
LOADING_ART_PATH = PROJECT_ROOT / "assets" / "art" / "loading_art.txt"
ERROR_ART_PATH = PROJECT_ROOT / "assets" / "art" / "error_art.txt"
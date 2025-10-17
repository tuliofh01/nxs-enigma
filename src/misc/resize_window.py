#! python3

from src.misc.config import CONFIG

# Resizes window to appropriate dimensions.
height = CONFIG["tui"]["default_height"]
width = CONFIG["tui"]["default_width"]
print(f"\x1b[8;{height};{width}t")
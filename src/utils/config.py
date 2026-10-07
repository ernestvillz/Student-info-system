import json
from pathlib import Path
from typing import Any, Dict


def load_config(config_path: str = "config/config.json") -> Dict[str, Any]:
    """Load application settings from an external JSON configuration file."""
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

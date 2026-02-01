import json
from pathlib import Path


def load_config(path):
    """Load the framework JSON configuration from disk."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_adf_config(config):
    """Return the ADF section of the config."""
    return config.get("adf", {})


def get_medallion_config(config):
    """Return the medallion section of the config."""
    return config.get("medallion", {})

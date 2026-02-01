import json
from pathlib import Path


def load_config(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_adf_config(config):
    return config.get("adf", {})


def get_medallion_config(config):
    return config.get("medallion", {})

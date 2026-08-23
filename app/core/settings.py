"""Persistent user-configurable device settings."""

import json
from pathlib import Path


SETTINGS_PATH = Path(__file__).resolve().parents[2] / "books" / "data" / "settings.json"


def load():
    try:
        with SETTINGS_PATH.open("r", encoding="utf-8") as file:
            settings = json.load(file)
        return settings if isinstance(settings, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def get_font_path(default_path):
    return load().get("font_path", default_path)


def save_font_path(font_path):
    settings = load()
    settings["font_path"] = str(font_path)
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SETTINGS_PATH.open("w", encoding="utf-8") as file:
        json.dump(settings, file, indent=2)

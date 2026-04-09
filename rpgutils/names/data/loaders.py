"""
Contains functions for I/O functions for language and phoneme data
"""
import json
from pathlib import Path

import unicodedata

from .language_data import LanguageData


def _normalize(obj):
    """Recursively normalizes all strings in a JSON structure to NFC Unicode form.

    Args:
        obj: A string, list, dict, or other value from a parsed JSON structure.

    Returns:
        The same structure with all strings normalized to NFC.
    """
    if isinstance(obj, str):
        return unicodedata.normalize('NFC', obj)
    elif isinstance(obj, list):
        return [_normalize(item) for item in obj]
    elif isinstance(obj, dict):
        return {_normalize(k): _normalize(v) for k, v in obj.items()}
    return obj


def load_language(language_name: str) -> LanguageData:
    """Loads a language profile from the `languages` directory.

    Args:
        language_name: The name of the language to load (e.g. 'english', 'elvish').

    Returns:
        A fully populated LanguageData instance.

    Raises:
        FileNotFoundError: If the `languages` directory or language file does not exist.
    """
    languages_path = Path(__file__).parent / "languages"
    if not languages_path.exists():
        raise FileNotFoundError(f"Languages directory not found at {languages_path}")

    language_file = languages_path / f"{language_name}.json"
    if not language_file.exists():
        raise FileNotFoundError(f"Language file not found for {language_name}")

    with language_file.open(encoding="utf-8") as file:
        json_data = _normalize(json.load(file))

    return LanguageData.from_dict(json_data)

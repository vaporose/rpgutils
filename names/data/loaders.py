"""
Contains functions for I/O functions for language and phoneme data
"""
from pathlib import Path
import json
from .language_data import LanguageData, SyllableCount, SyllableStructure, SlotDefinition, TagInclusion, SoundInclusion, PositionData, PositionSet


def load_language(language_name: str) -> LanguageData:
    """
    Loads a language from the languages directory and handles file existence checks

    Args:
        language_name:

    Returns:

    """
    languages_path = Path(__file__).parent / "languages"
    if not languages_path.exists():
        raise FileNotFoundError(f"Languages directory not found at {languages_path}")

    language_file = languages_path / f"{language_name}.json"
    if not language_file.exists():
        raise FileNotFoundError(f"Language file not found for {language_name}")

    with language_file.open() as file:
        json_data = json.load(file)

    return LanguageData.from_dict(json_data)



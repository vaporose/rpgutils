import random
from typing import Literal

from .generator import Generator
from .defaults import DEFAULT_RARITY_CONFIG
from .rarity_config import RarityConfig
from ..data.list_data import ListData, ListEntry
from ..data.loaders import load_list


class ListGenerator(Generator):
    """
    Generator that selects from a curated list of words.

    Loads a bundled word list by language and source, optionally merged with
    or replaced by user-provided entries. Candidates are pre-filtered at
    construction time by grammar and/or context tags.

    Attributes:
        _candidates: Pre-filtered list of value strings to draw from.
    """

    def __init__(
        self,
        language: str,
        source: str,
        grammar: list[str] | None = None,
        context: list[str] | None = None,
        user_entries: list[dict] | None = None,
        user_mode: Literal["additive", "override"] = "additive",
        rarity_config: RarityConfig = DEFAULT_RARITY_CONFIG,
    ):
        """
        Args:
            language: Language folder to load from (e.g. 'english').
            source: List file to load, without extension (e.g. 'nautical').
            grammar: Grammatical role filter. Values: 'noun', 'adjective', 'prefix', 'suffix'.
            context: Semantic context filter (e.g. 'geographic', 'nautical').
            user_entries: Additional entries in list-entry dict format.
            user_mode: 'additive' merges user entries with bundled; 'override' replaces bundled entirely.
            rarity_config: Rarity configuration (inherited from Generator base).

        Raises:
            FileNotFoundError: If the bundled list does not exist and user_mode is not 'override'.
            ValueError: If no candidates remain after filtering.
        """
        super().__init__(rarity_config)

        if user_mode == "override" and user_entries:
            data = ListData([ListEntry.from_dict(e) for e in user_entries])
        else:
            data = load_list(language, source)
            if user_entries:
                user_data = ListData([ListEntry.from_dict(e) for e in user_entries])
                data = data.merge(user_data)

        self._candidates = data.candidates(grammar=grammar, context=context)

        if not self._candidates:
            raise ValueError(
                f"No candidates found for language={language!r}, source={source!r}, "
                f"grammar={grammar}, context={context}"
            )

    def generate(self) -> str:
        return random.choice(self._candidates)

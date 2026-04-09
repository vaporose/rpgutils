"""
Generator for phonetic names based on a language profile.

Language data is found under `names/data/languages/`.
"""

import random

from .generator import Generator
from ..data import LanguageData, load_language, PHONEMES


class PhoneticGenerator(Generator):
    """
    Generator for phonetic names based on a language profile.

    Example:
    >>> generator = PhoneticGenerator("english")
    >>> name = generator.generate()
    >>> print(name)
    """

    def __init__(self, language: str = "english"):
        super().__init__()
        self.language_data: LanguageData = load_language(language)

    def generate(self) -> str:
        """
        Main entry point for generating names.
        Returns:
            A generated name string based on the language profile.
        """
        syllable_count = random.randint(
            self.language_data.syllable_count.min,
            self.language_data.syllable_count.max,
        )
        return "".join(self.generate_syllable() for _ in range(syllable_count))

    def generate_syllable(self) -> str:
        """
        Generates a single syllable based on the language profile.
        Returns:
            A generated syllable string.
        """
        patterns = []
        weights = []
        for structure in self.language_data.syllable_structures:
            patterns.append(structure.pattern)
            weights.append(self.tiers.get(structure.tier, 1.0))
        pattern = random.choices(patterns, weights=weights, k=1)[0]
        syllable = "".join(self.generate_phoneme(slot.slot) for slot in pattern)
        return syllable

    def generate_phoneme(self, slot: str) -> str:
        """
        Generates a single phoneme for the given syllable position.

        Args:
            slot: The position to generate for. One of: 'onset', 'nucleus', 'coda'.

        Returns:
            A generated phoneme string.
        """
        position_data = getattr(self.language_data.positions, slot)
        exclude_set = set(position_data.exclude)

        candidates, weights = self._collect_tag_sounds(position_data.include_tags, exclude_set)
        self._collect_explicit_sounds(position_data.include, exclude_set, candidates, weights)

        if not candidates:
            return ""

        return random.choices(candidates, weights=weights, k=1)[0]

    def _collect_tag_sounds(
        self, include_tags: list, exclude_set: set
    ) -> tuple[list[str], list[float]]:
        """
        Builds a candidate pool from tag-based inclusions.

        Args:
            include_tags: List of TagInclusion objects from the language profile.
            exclude_set: Set of sounds to exclude.

        Returns:
            A tuple of (candidates, weights) parallel lists.
        """
        candidates: list[str] = []
        weights: list[float] = []
        seen: set[str] = set()
        for tag_inclusion in include_tags:
            tier_weight = self.tiers.get(tag_inclusion.tier, 1.0)
            for sound in PHONEMES.get(tag_inclusion.tag, []):
                if sound not in seen and sound not in exclude_set:
                    candidates.append(sound)
                    weights.append(tier_weight)
                    seen.add(sound)
        return candidates, weights

    def _collect_explicit_sounds(
        self, include: list, exclude_set: set, candidates: list, weights: list
    ) -> None:
        """
        Appends explicitly included sounds to an existing candidate pool.

        Mutates candidates and weights in place.

        Args:
            include: List of SoundInclusion objects from the language profile.
            exclude_set: Set of sounds to exclude.
            candidates: Existing candidate list to append to.
            weights: Existing weights list to append to.
        """
        seen: set[str] = set(candidates)
        for sound_inclusion in include:
            if sound_inclusion.sound not in seen and sound_inclusion.sound not in exclude_set:
                candidates.append(sound_inclusion.sound)
                weights.append(self.tiers.get(sound_inclusion.tier, 1.0))
                seen.add(sound_inclusion.sound)

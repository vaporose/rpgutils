"""
Base class for all generators.

This will not have any use if implemented directly, as the `generate` method has no implementation.

Use the specific generator types (phonetic, compositional, mutated) for actual name generation.
"""

from abc import ABC, abstractmethod

from .rarity_tier_config import RarityConfig
from .defaults import DEFAULT_RARITY_CONFIG


class Generator(ABC):
    """
    Abstract base class for all name generators.

    A Generator is responsible for producing a single string component of a name.
    Subclasses implement a specific generation strategy: phonetic, compositional, or mutated.

    Attributes:
        tiers: Mapping of tier name to weight, built from the provided RarityConfig.
    """

    def __init__(self, rarity_config: RarityConfig = DEFAULT_RARITY_CONFIG):
        self.tiers = rarity_config.build()

    @abstractmethod
    def generate(self) -> str:
        """Generate and return a name string.

        Returns:
            A generated name component as a string.
        """
        pass

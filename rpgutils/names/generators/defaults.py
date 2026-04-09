"""
Defaults all default configuration options to be used across the generators.

This will generally pertain to generation parameters that are shared across multiple generator types, such as rarity
tiers and decay values.
"""

from .rarity_config import RarityConfig


DEFAULT_RARITY_CONFIG = RarityConfig(
    tiers=["common", "uncommon", "rare"],
    decay=0.5
)

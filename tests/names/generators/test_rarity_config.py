import pytest
from rpgutils.names.generators.rarity_config import RarityConfig


def test_build_weights():
    """build() produces correct exponential decay weights for each tier."""
    config = RarityConfig(tiers=["common", "uncommon", "rare"], decay=0.5)
    weights = config.build()

    assert weights["common"] == 1.0
    assert weights["uncommon"] == 0.5
    assert weights["rare"] == 0.25


def test_build_first_tier_always_one():
    """The first tier always has weight 1.0 regardless of decay value."""
    config = RarityConfig(tiers=["common", "uncommon"], decay=0.25)
    assert config.build()["common"] == 1.0


def test_build_equal_weights_at_decay_one():
    """A decay of 1.0 produces equal weights across all tiers."""
    config = RarityConfig(tiers=["common", "uncommon", "rare"], decay=1.0)
    weights = config.build()

    assert weights["common"] == weights["uncommon"] == weights["rare"] == 1.0


def test_decay_rejects_zero():
    with pytest.raises(ValueError):
        RarityConfig(tiers=["common"], decay=0.0)


def test_decay_rejects_negative():
    with pytest.raises(ValueError):
        RarityConfig(tiers=["common"], decay=-0.5)


def test_decay_rejects_greater_than_one():
    with pytest.raises(ValueError):
        RarityConfig(tiers=["common"], decay=1.5)


def test_decay_accepts_upper_boundary():
    """decay=1.0 is valid."""
    config = RarityConfig(tiers=["common"], decay=1.0)
    assert config.decay == 1.0

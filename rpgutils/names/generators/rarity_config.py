from dataclasses import dataclass


@dataclass
class RarityConfig:
    """
    Configuration for rarity tiers and decay values.

    Attributes:
        tiers (list[str]): Ordered list of tier names from most to least common.
        decay (float): Decay ratio between each tier, default is 0.5.
    """
    tiers: list[str]  # ordered most-to-least common
    decay: float = 0.5  # ratio between each tier

    def __post_init__(self):
        if not (0 < self.decay <= 1):
            raise ValueError(f"decay must be between 0 (exclusive) and 1 (inclusive), got {self.decay}")

    def build(self) -> dict[str, float]:
        """
        Builds a dictionary mapping tiers to their corresponding weighted decay values.

        This method calculates a decay value for each tier using an exponential
        decay formula. The tier is associated with the calculated decay value in the
        resulting dictionary.

        Returns:
            dict[str, float]: A dictionary where keys are tier names and values are
            their corresponding decay values.
        """
        return {tier: self.decay ** i for i, tier in enumerate(self.tiers)}

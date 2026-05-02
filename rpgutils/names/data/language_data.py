from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class SyllableCount:
    """The minimum and maximum number of syllables for a generated name.

    Attributes:
        min: Minimum number of syllables.
        max: Maximum number of syllables.
    """
    min: int
    max: int

    @classmethod
    def from_dict(cls, data: dict) -> SyllableCount:
        return cls(min=data["min"], max=data["max"])


@dataclass
class SlotDefinition:
    """A single positional slot within a syllable structure.

    Attributes:
        slot: The position this slot represents. One of: 'onset', 'nucleus', 'coda'.
    """
    slot: str

    @classmethod
    def from_dict(cls, data: dict) -> SlotDefinition:
        return cls(slot=data["slot"])


@dataclass
class SyllableStructure:
    """A syllable pattern and its relative frequency tier.

    The pattern is an ordered list of SlotDefinitions describing which positions
    are present in this syllable shape. For example, a CVC syllable would be:
        [SlotDefinition('onset'), SlotDefinition('nucleus'), SlotDefinition('coda')]

    Attributes:
        pattern: Ordered list of slot definitions for this syllable shape.
        tier: Relative frequency tier (e.g. 'common', 'uncommon', 'rare').
    """
    pattern: list[SlotDefinition]
    tier: str

    @classmethod
    def from_dict(cls, data: dict) -> SyllableStructure:
        return cls(
            pattern=[SlotDefinition.from_dict(s) for s in data["pattern"]],
            tier=data["tier"],
        )


@dataclass
class TagInclusion:
    """A phoneme tag to include, paired with a frequency tier.

    All phonemes in the registry carrying this tag will be pulled into the
    position's candidate pool at the specified tier.

    Attributes:
        tag: The phoneme tag to match against the registry.
        tier: Relative frequency tier for all matched phonemes.
    """
    tag: str
    tier: str

    @classmethod
    def from_dict(cls, data: dict) -> TagInclusion:
        return cls(tag=data["tag"], tier=data["tier"])


@dataclass
class SoundInclusion:
    """An explicit phoneme sound to include, paired with a frequency tier.

    Used to add specific sounds that would not be captured by tag-based
    inclusion, or to assign a different tier to a sound than its tag would give.

    Attributes:
        sound: The exact phoneme sound string.
        tier: Relative frequency tier for this sound.
    """
    sound: str
    tier: str

    @classmethod
    def from_dict(cls, data: dict) -> SoundInclusion:
        return cls(sound=data["sound"], tier=data["tier"])


@dataclass
class PositionData:
    """The full phoneme specification for a single syllable position.

    Phonemes are resolved by first collecting all sounds matching any tag in
    include_tags, then adding any explicit sounds in include, then removing
    any sounds listed in exclude.

    Attributes:
        include_tags: Tag-based inclusions, each with a frequency tier.
        include: Explicit sound inclusions, each with a frequency tier.
        exclude: Explicit sound strings to remove from the candidate pool.
    """
    include_tags: list[TagInclusion] = field(default_factory=list)
    include: list[SoundInclusion] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> PositionData:
        return cls(
            include_tags=[TagInclusion.from_dict(t) for t in data.get("include_tags", [])],
            include=[SoundInclusion.from_dict(s) for s in data.get("include", [])],
            exclude=data.get("exclude", []),
        )


@dataclass
class PositionSet:
    """The phoneme specifications for all three syllable positions.

    Attributes:
        onset: Consonant(s) that open a syllable.
        nucleus: Vowel(s) at the core of a syllable.
        coda: Consonant(s) that close a syllable.
    """
    onset: PositionData = field(default_factory=PositionData)
    nucleus: PositionData = field(default_factory=PositionData)
    coda: PositionData = field(default_factory=PositionData)

    @classmethod
    def from_dict(cls, data: dict) -> PositionSet:
        return cls(
            onset=PositionData.from_dict(data["onset"]),
            nucleus=PositionData.from_dict(data["nucleus"]),
            coda=PositionData.from_dict(data["coda"]),
        )


@dataclass
class LanguageData:
    """The complete phonetic profile for a language.

    Attributes:
        name: The identifier for this language (e.g. 'elvish', 'japanese').
        syllable_count: The min/max syllable count per generated name.
        syllable_structures: Weighted list of valid syllable patterns.
        positions: Phoneme specifications for onset, nucleus, and coda positions.
    """
    name: str
    syllable_count: SyllableCount
    syllable_structures: list[SyllableStructure]
    positions: PositionSet

    @classmethod
    def from_dict(cls, data: dict) -> LanguageData:
        return cls(
            name=data["name"],
            syllable_count=SyllableCount.from_dict(data["syllable_count"]),
            syllable_structures=[SyllableStructure.from_dict(s) for s in data["syllable_structures"]],
            positions=PositionSet.from_dict(data["positions"]),
        )

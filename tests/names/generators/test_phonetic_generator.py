import pytest
from rpgutils.names.generators.phonetic_generator import PhoneticGenerator


def test_generate_names():
    """Verifies the phonetic generator correctly returns a string when instantiated with a valid language."""
    generator = PhoneticGenerator("english")
    name = generator.generate()
    assert name is not None
    assert isinstance(name, str)


def test_english_nucleus_excludes_invalid_sounds():
    """
    This is a generic test of how the excluded sounds function.

    Although exclusions occur in other languages as well as in the other two phonetic positions,
    the functionality is the same across all. This is a functional test that the exclusion works,
    not a test of the specific excluded sounds, so we only test one position in one language.
    """
    generator = PhoneticGenerator("english")
    position_data = generator.language_data.positions.nucleus
    exclude_set = set(position_data.exclude)
    candidates, _ = generator._collect_tag_sounds(position_data.include_tags, exclude_set)

    assert "ï" not in candidates
    assert "ae" not in candidates


def test_explicit_include_respects_exclude():
    """Sounds in the explicit include list that also appear in exclude should not be added to the pool."""
    generator = PhoneticGenerator("english")
    position_data = generator.language_data.positions.nucleus
    exclude_set = set(position_data.exclude)

    candidates, weights = generator._collect_tag_sounds(position_data.include_tags, exclude_set)
    generator._collect_explicit_sounds(position_data.include, exclude_set, candidates, weights)

    for sound in position_data.exclude:
        assert sound not in candidates


def test_explicit_include_no_duplicates():
    """Sounds already added via tag inclusion should not be added again by explicit inclusion."""
    generator = PhoneticGenerator("english")
    position_data = generator.language_data.positions.onset
    exclude_set = set(position_data.exclude)

    candidates, weights = generator._collect_tag_sounds(position_data.include_tags, exclude_set)
    generator._collect_explicit_sounds(position_data.include, exclude_set, candidates, weights)

    assert len(candidates) == len(set(candidates))


def test_empty_candidates_raises():
    """A language profile that resolves to no candidates for a slot should raise a ValueError."""
    from rpgutils.names.data.language_data import (
        LanguageData, SyllableCount, SyllableStructure, SlotDefinition, PositionSet, PositionData
    )

    generator = PhoneticGenerator("english")
    generator.language_data = LanguageData(
        name="empty_test",
        syllable_count=SyllableCount(min=1, max=1),
        syllable_structures=[SyllableStructure(pattern=[SlotDefinition("nucleus")], tier="common")],
        positions=PositionSet(nucleus=PositionData(include_tags=[], include=[], exclude=[])),
    )

    with pytest.raises(ValueError, match="No phoneme candidates for slot 'nucleus'"):
        generator.generate()

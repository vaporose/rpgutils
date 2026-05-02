import pytest

from rpgutils.names.generators.list_generator import ListGenerator


SAMPLE_ENTRIES = [
    {"value": "Storm", "context": ["nautical"], "grammar": ["noun", "adjective"]},
    {"value": "Relentless", "context": ["nautical"], "grammar": ["adjective"]},
    {"value": "Anchor", "context": ["nautical"], "grammar": ["noun"]},
    {"value": "Vale", "context": ["geographic"], "grammar": ["noun"]},
]


def override_generator(**kwargs) -> ListGenerator:
    """Build a ListGenerator from SAMPLE_ENTRIES with no filesystem access."""
    return ListGenerator(
        language="fake",
        source="fake",
        user_entries=SAMPLE_ENTRIES,
        user_mode="override",
        **kwargs,
    )


def test_generate_returns_string():
    gen = override_generator()
    assert isinstance(gen.generate(), str)


def test_generate_returns_value_from_list():
    gen = override_generator()
    all_values = {e["value"] for e in SAMPLE_ENTRIES}
    assert gen.generate() in all_values


def test_grammar_filter_noun():
    gen = override_generator(grammar=["noun"])
    nouns = {"Storm", "Anchor", "Vale"}
    for _ in range(20):
        assert gen.generate() in nouns


def test_grammar_filter_adjective():
    gen = override_generator(grammar=["adjective"])
    adjectives = {"Storm", "Relentless"}
    for _ in range(20):
        assert gen.generate() in adjectives


def test_context_filter():
    gen = override_generator(context=["geographic"])
    for _ in range(20):
        assert gen.generate() == "Vale"


def test_grammar_and_context_filter_intersect():
    gen = override_generator(grammar=["noun"], context=["nautical"])
    nautical_nouns = {"Storm", "Anchor"}
    for _ in range(20):
        assert gen.generate() in nautical_nouns


def test_empty_candidates_raises():
    with pytest.raises(ValueError):
        override_generator(grammar=["suffix"])


def test_user_entries_additive_extends_pool():
    extra = [{"value": "Thunderclad", "context": ["nautical"], "grammar": ["noun"]}]
    gen = ListGenerator(
        language="english",
        source="nautical",
        grammar=["noun"],
        user_entries=extra,
        user_mode="additive",
    )
    results = {gen.generate() for _ in range(50)}
    assert "Thunderclad" in results


def test_user_entries_override_replaces_bundled():
    only_entry = [{"value": "OnlyThis", "context": ["nautical"], "grammar": ["noun"]}]
    gen = ListGenerator(
        language="fake",
        source="fake",
        user_entries=only_entry,
        user_mode="override",
    )
    for _ in range(10):
        assert gen.generate() == "OnlyThis"


def test_missing_language_raises():
    with pytest.raises(FileNotFoundError):
        ListGenerator(language="nonexistent", source="nautical")


def test_missing_source_raises():
    with pytest.raises(FileNotFoundError):
        ListGenerator(language="english", source="nonexistent")

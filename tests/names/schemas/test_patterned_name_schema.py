import pytest

from rpgutils.names.generators import Generator
from rpgutils.names.schemas.name_schema import NamePart
from rpgutils.names.schemas.patterned_name_schema import NamePattern, PatternedNameSchema, ShipName


class FixedGenerator(Generator):
    def __init__(self, value: str):
        super().__init__()
        self._value = value

    def generate(self) -> str:
        return self._value


class CountingGenerator(Generator):
    def __init__(self):
        super().__init__()
        self._count = 0

    def generate(self) -> str:
        self._count += 1
        return f"value{self._count}"


def make_schema(template: str, capitalize_slots: bool = True, **roles: str) -> PatternedNameSchema:
    """Build a single-pattern PatternedNameSchema with FixedGenerators."""
    parts = [NamePart(FixedGenerator(value), role) for role, value in roles.items()]
    return PatternedNameSchema(
        patterns={"default": NamePattern(template=template, parts=parts, capitalize_slots=capitalize_slots)}
    )


def test_template_applied():
    schema = make_schema("The {adjective} {noun}", adjective="relentless", noun="tide")
    assert schema.full_name == "The Relentless Tide"


def test_slot_values_capitalized():
    schema = make_schema("{adjective} {noun}", adjective="bold", noun="storm")
    parts = schema.full_name.split()
    assert all(p[0].isupper() for p in parts if p.isalpha())


def test_literal_text_preserved():
    schema = make_schema("Forest of {noun}", noun="shadow")
    assert schema.full_name == "Forest of Shadow"
    assert schema.full_name.startswith("Forest of")


def test_compound_capitalizes_first_char_only():
    schema = make_schema("{adjective}{noun}", capitalize_slots=False, adjective="iron", noun="tide")
    assert schema.full_name == "Irontide"


def test_regenerate_updates_values():
    generator = CountingGenerator()
    schema = PatternedNameSchema(
        patterns={"default": NamePattern(template="{word}", parts=[NamePart(generator, "word")])}
    )
    first = schema.full_name
    schema.regenerate()
    assert schema.full_name != first


def test_callable_returns_full_name():
    schema = make_schema("{adjective} {noun}", adjective="swift", noun="wave")
    assert schema() == schema.full_name


def test_str_returns_full_name():
    schema = make_schema("{adjective} {noun}", adjective="swift", noun="wave")
    assert str(schema) == schema.full_name


def test_repr_format():
    schema = make_schema("{adjective} {noun}", adjective="swift", noun="wave")
    assert repr(schema) == f"PatternedNameSchema('{schema.full_name}')"


def test_role_access_by_attribute():
    schema = make_schema("{adjective} {noun}", adjective="bold", noun="anchor")
    assert schema.adjective == "bold"
    assert schema.noun == "anchor"


def test_single_slot_template():
    schema = make_schema("The {noun}", noun="tempest")
    assert schema.full_name == "The Tempest"


def test_multiple_patterns_all_allowed_by_default():
    schema = PatternedNameSchema(patterns={
        "a": NamePattern("{word}", [NamePart(FixedGenerator("alpha"), "word")]),
        "b": NamePattern("{word}", [NamePart(FixedGenerator("beta"), "word")]),
    })
    results = set()
    for _ in range(30):
        schema.regenerate()
        results.add(schema.full_name)
    assert len(results) > 1


def test_allowed_restricts_patterns():
    schema = PatternedNameSchema(
        patterns={
            "a": NamePattern("{word}", [NamePart(FixedGenerator("alpha"), "word")]),
            "b": NamePattern("{word}", [NamePart(FixedGenerator("beta"), "word")]),
        },
        allowed=["a"],
    )
    for _ in range(10):
        schema.regenerate()
        assert schema.full_name == "Alpha"


def test_unknown_allowed_pattern_raises():
    with pytest.raises(ValueError):
        PatternedNameSchema(
            patterns={"a": NamePattern("{word}", [NamePart(FixedGenerator("x"), "word")])},
            allowed=["nonexistent"],
        )


class TestShipName:
    def test_generates_string(self):
        assert isinstance(str(ShipName()), str)

    def test_title_pattern(self):
        ship = ShipName(allowed=["title"])
        result = str(ship)
        assert result.startswith("The ")
        assert len(result.split()) == 2

    def test_emblem_pattern(self):
        ship = ShipName(allowed=["emblem"])
        result = str(ship)
        assert result.startswith("The ")
        assert len(result.split()) == 2

    def test_classic_pattern(self):
        ship = ShipName(allowed=["classic"])
        result = str(ship)
        assert result.startswith("The ")
        assert len(result.split()) == 3

    def test_poetic_pattern(self):
        ship = ShipName(allowed=["poetic"])
        result = str(ship)
        assert result.startswith("The ")
        assert " of the " in result

    def test_compound_pattern(self):
        ship = ShipName(allowed=["compound"])
        result = str(ship)
        assert not result.startswith("The ")
        assert result[0].isupper()
        assert " " not in result

    def test_invalid_allowed_raises(self):
        with pytest.raises(ValueError):
            ShipName(allowed=["nonexistent"])

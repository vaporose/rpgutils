import pytest

from rpgutils.names.generators import Generator
from rpgutils.names.schemas.name_schema import NamePart, NameSchema


class FixedGenerator(Generator):
    """
    A deterministic generator that always returns the same value.
    Used to isolate NameSchema from generation logic.
    """

    def __init__(self, value: str):
        super().__init__()
        self._value = value

    def generate(self) -> str:
        return self._value


class CountingGenerator(Generator):
    """A generator that returns incrementing values. Used to verify regenerate produces updated output."""

    def __init__(self):
        super().__init__()
        self._count = 0

    def generate(self) -> str:
        self._count += 1
        return f"value{self._count}"


def test_parts_are_generated_on_init():
    """Parts have non-empty values immediately after instantiation."""
    schema = NameSchema(parts=[NamePart(FixedGenerator("arath"), "first")])
    assert schema.first != ""


def test_role_access():
    """Part values are accessible as attributes by their role name."""
    schema = NameSchema(parts=[
        NamePart(FixedGenerator("arath"), "first"),
        NamePart(FixedGenerator("ondrel"), "last"),
    ])
    assert schema.first == "arath"
    assert schema.last == "ondrel"


def test_unknown_role_raises_attribute_error():
    schema = NameSchema(parts=[NamePart(FixedGenerator("arath"), "first")])
    with pytest.raises(AttributeError):
        _ = schema.middle


def test_full_name_default_separator():
    """Parts are joined with a space by default."""
    schema = NameSchema(parts=[
        NamePart(FixedGenerator("arath"), "first"),
        NamePart(FixedGenerator("ondrel"), "last"),
    ])
    assert schema.full_name == "Arath Ondrel"


def test_full_name_custom_separator():
    schema = NameSchema(
        parts=[
            NamePart(FixedGenerator("arath"), "first"),
            NamePart(FixedGenerator("ondrel"), "last"),
        ],
        separator="-",
    )
    assert schema.full_name == "Arath-Ondrel"


def test_capitalization():
    """First character of each part is capitalized."""
    schema = NameSchema(parts=[
        NamePart(FixedGenerator("arath"), "first"),
        NamePart(FixedGenerator("ondrel"), "last"),
    ])
    assert schema.full_name[0].isupper()
    parts = schema.full_name.split(" ")
    assert all(p[0].isupper() for p in parts)


def test_regenerate_updates_values():
    """regenerate() produces new values from the generator."""
    generator = CountingGenerator()
    schema = NameSchema(parts=[NamePart(generator, "first")])
    first_value = schema.first
    schema.regenerate()
    assert schema.first != first_value


def test_callable_returns_full_name():
    schema = NameSchema(parts=[NamePart(FixedGenerator("arath"), "first")])
    assert schema() == schema.full_name


def test_str_returns_full_name():
    schema = NameSchema(parts=[NamePart(FixedGenerator("arath"), "first")])
    assert str(schema) == schema.full_name


def test_repr_format():
    schema = NameSchema(parts=[NamePart(FixedGenerator("arath"), "first")])
    assert repr(schema) == f"NameSchema('{schema.full_name}')"


def test_integration_with_phonetic_generator():
    """NameSchema produces a non-empty string when backed by a real PhoneticGenerator."""
    from rpgutils.names.generators.phonetic_generator import PhoneticGenerator
    schema = NameSchema(parts=[
        NamePart(PhoneticGenerator("english"), "first"),
        NamePart(PhoneticGenerator("english"), "last"),
    ])
    assert isinstance(schema.full_name, str)
    assert len(schema.full_name) > 0

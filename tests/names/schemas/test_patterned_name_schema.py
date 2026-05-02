import pytest

from rpgutils.names.generators import Generator
from rpgutils.names.schemas.name_schema import NamePart
from rpgutils.names.schemas.patterned_name_schema import PatternedNameSchema


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


def make_schema(template: str, **roles: str) -> PatternedNameSchema:
    """Helper: build a PatternedNameSchema with FixedGenerators keyed by role."""
    parts = [NamePart(FixedGenerator(value), role) for role, value in roles.items()]
    return PatternedNameSchema(template=template, parts=parts)


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


def test_compound_template_no_spaces():
    schema = make_schema("{adjective}{noun}", adjective="iron", noun="haven")
    assert schema.full_name == "IronHaven"


def test_regenerate_updates_values():
    generator = CountingGenerator()
    schema = PatternedNameSchema(
        template="{word}",
        parts=[NamePart(generator, "word")],
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

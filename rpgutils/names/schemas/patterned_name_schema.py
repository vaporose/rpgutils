from .name_schema import NameSchema, NamePart
from .string_utilities import capitalize
from ..generators.list_generator import ListGenerator


class PatternedNameSchema(NameSchema):
    """A NameSchema that combines parts according to a template string.

    Slot values are referenced in the template by their role name using
    standard Python format syntax: "{adjective} {noun}".
    Literal text in the template is preserved as-is; only slot values
    are capitalized.

    Subclasses pre-wire the template and parts for a specific name type.
    """

    def __init__(self, template: str, parts: list[NamePart]):
        self._template = template
        super().__init__(parts=parts)

    @property
    def full_name(self) -> str:
        values = {part.role: capitalize(part.value, {0}) for part in self._parts}
        return self._template.format(**values)


class ShipName(PatternedNameSchema):
    """A nautical ship name in the form '{adjective} {noun}'."""

    def __init__(self, language: str = "english"):
        super().__init__(
            template="{adjective} {noun}",
            parts=[
                NamePart(ListGenerator(language, "nautical", grammar=["adjective"]), "adjective"),
                NamePart(ListGenerator(language, "nautical", grammar=["noun"]), "noun"),
            ],
        )


class InnName(PatternedNameSchema):
    """An inn name in the form 'The {adjective} {noun}'."""

    def __init__(self, language: str = "english"):
        super().__init__(
            template="The {adjective} {noun}",
            parts=[
                NamePart(ListGenerator(language, "inn", grammar=["adjective"]), "adjective"),
                NamePart(ListGenerator(language, "inn", grammar=["noun"]), "noun"),
            ],
        )


class ShopName(PatternedNameSchema):
    """A shop name in the form '{noun} & {noun2}'."""

    def __init__(self, language: str = "english"):
        super().__init__(
            template="{noun} & {noun2}",
            parts=[
                NamePart(ListGenerator(language, "shop", grammar=["noun"]), "noun"),
                NamePart(ListGenerator(language, "shop", grammar=["noun"]), "noun2"),
            ],
        )


class ItemName(PatternedNameSchema):
    """An item name in the form '{adjective} {noun}'."""

    def __init__(self, language: str = "english"):
        super().__init__(
            template="{adjective} {noun}",
            parts=[
                NamePart(ListGenerator(language, "items", grammar=["adjective"]), "adjective"),
                NamePart(ListGenerator(language, "items", grammar=["noun"]), "noun"),
            ],
        )

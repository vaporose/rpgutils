from dataclasses import dataclass, field

from names.generators import Generator


@dataclass
class NamePart:
    """A single component of a name, pairing a generator with a semantic role.

    Attributes:
        generator: The Generator instance responsible for producing this part.
        role: A label describing this part's role (e.g. 'first', 'last', 'title').
        value: The most recently generated string for this part. Populated on generation.
    """
    generator: Generator
    role: str
    value: str = field(default='', init=False)


class NameSchema:
    """
    Defines the structure of a name and orchestrates its generation.

    A NameSchema holds an ordered list of NameParts, each backed by a Generator.
    Parts are generated on instantiation and can be regenerated at any time.

    Subclasses pre-configure parts and separators to represent specific name types
    (e.g., PersonName, CityName). Direct instantiation is also valid for custom schemas.

    Individual parts are accessible as attributes by their role:
        name.first -> the value of the part with role 'first'

    The full name string is available via str(), repr(), or calling the instance directly.

    Attributes:
        _parts: Ordered list of NameParts defining the structure of this name.
        _separator: String used to join parts into the full name.
    """

    def __init__(self, parts: list[NamePart], separator: str = ' '):
        """
        Initializes the schema and generates all parts immediately.

        Args:
            parts: Ordered list of NameParts defining the structure of this name.
            separator: String used to join parts into the full name. Defaults to a space.
        """
        self._parts = parts
        self._separator = separator
        self.regenerate()

    def regenerate(self):
        """Re-runs all generators, updating each part's value."""
        for part in self._parts:
            part.value = part.generator.generate()

    def __getattr__(self, name: str) -> str:
        for part in self._parts:
            if part.role == name:
                return part.value
        raise AttributeError(f"'{type(self).__name__}' has no name part '{name}'")

    @property
    def full_name(self) -> str:
        """The complete name string, with all parts joined by the separator."""
        return self._separator.join(part.value for part in self._parts)

    def __call__(self) -> str:
        return self.full_name

    def __str__(self) -> str:
        return self.full_name

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.full_name!r})"

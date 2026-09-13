from ..name_schema import NamePart
from ...generators.list_generator import ListGenerator
from .base import NamePattern, PatternedNameSchema


class ShipName(PatternedNameSchema):
    """Generates a ship name using one of several named structural patterns.

    Patterns:
        ``title``
            ``"The {adjective}"`` — a single evocative adjective standing alone.

            Examples: *The Dauntless*, *The Relentless*, *The Fearless*

        ``emblem``
            ``"The {noun}"`` — a single powerful noun standing alone.

            Examples: *The Tempest*, *The Horizon*, *The Sovereign*

        ``classic``
            ``"The {adjective} {noun}"`` — an adjective paired with a noun.

            Examples: *The Crimson Tide*, *The Iron Wake*, *The Golden Horizon*

        ``poetic``
            ``"The {concept} of the {element}"`` — an abstract concept joined
            to a natural force.

            Examples: *The Heart of the Storm*, *The Eye of the Gale*,
            *The Lady of the Tide*

        ``compound``
            ``"{adjective}{noun}"`` — two words merged without a separator or
            article. Only the first character of the result is capitalized.

            Examples: *Irontide*, *Swiftstorm*, *Crimsongale*

    Args:
        language: The language corpus to draw words from. Defaults to ``"english"``.
        allowed: Pattern names to draw from. ``None`` means all five patterns
            are used with equal probability. Pass a list to restrict generation
            to specific structures.

            Valid values: ``"title"``, ``"emblem"``, ``"classic"``,
            ``"poetic"``, ``"compound"``

    Example::

        ShipName()                                  # any pattern
        ShipName(allowed=["title", "classic"])      # only title and classic
        ShipName(allowed=["compound"])              # always compound
    """

    def __init__(self, language: str = "english", allowed: list[str] | None = None):
        super().__init__(
            patterns={
                "title": NamePattern(
                    template="The {adjective}",
                    parts=[
                        NamePart(ListGenerator(language, "nautical", grammar=["adjective"]), "adjective"),
                    ],
                ),
                "emblem": NamePattern(
                    template="The {noun}",
                    parts=[
                        NamePart(ListGenerator(language, "nautical", grammar=["noun"], context=["nautical"]), "noun"),
                    ],
                ),
                "classic": NamePattern(
                    template="The {adjective} {noun}",
                    parts=[
                        NamePart(ListGenerator(language, "nautical", grammar=["adjective"]), "adjective"),
                        NamePart(ListGenerator(language, "nautical", grammar=["noun"], context=["nautical"]), "noun"),
                    ],
                ),
                "poetic": NamePattern(
                    template="The {concept} of the {element}",
                    parts=[
                        NamePart(ListGenerator(language, "nautical", context=["concept"]), "concept"),
                        NamePart(ListGenerator(language, "nautical", grammar=["noun"], context=["nautical"]), "element"),
                    ],
                ),
                "compound": NamePattern(
                    template="{adjective}{noun}",
                    parts=[
                        NamePart(ListGenerator(language, "nautical", grammar=["adjective"]), "adjective"),
                        NamePart(ListGenerator(language, "nautical", grammar=["noun"], context=["nautical"]), "noun"),
                    ],
                    capitalize_slots=False,
                ),
            },
            allowed=allowed,
        )

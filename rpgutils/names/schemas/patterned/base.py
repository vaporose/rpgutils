from __future__ import annotations

import random
from dataclasses import dataclass

from ..name_schema import NameSchema, NamePart
from ..string_utilities import capitalize


@dataclass
class NamePattern:
    """A single named structural variant within a PatternedNameSchema.

    Attributes:
        template: A format string with role names as placeholders,
            e.g. ``"The {adjective} {noun}"``.
        parts: The NameParts supplying values for each placeholder.
        capitalize_slots: When True (default), the first character of each
            slot value is capitalized before insertion. When False, only the
            first character of the final assembled string is capitalized —
            used for compound patterns where internal capitals look wrong.
    """
    template: str
    parts: list[NamePart]
    capitalize_slots: bool = True


class PatternedNameSchema(NameSchema):
    """
    A NameSchema that selects from a set of named structural patterns on each generation.

    Each pattern owns its own template and parts. On ``regenerate()``, one pattern
    is chosen at random from the allowed set and all of its parts are re-generated.

    Subclasses pre-wire patterns for a specific name type and document each pattern
    by name so callers can restrict generation to specific structures via ``allowed``.
    """

    def __init__(
        self,
        patterns: dict[str, NamePattern],
        allowed: list[str] | None = None,
    ):
        """
        Args:
            patterns: Named structural patterns available for this schema.
            allowed: Pattern names to draw from. ``None`` means all patterns
                are used with equal probability.

        Raises:
            ValueError: If any name in ``allowed`` is not a key in ``patterns``.
        """
        self._named_patterns = patterns
        if allowed is not None:
            invalid = set(allowed) - set(patterns.keys())
            if invalid:
                raise ValueError(
                    f"Unknown pattern name(s): {invalid}. "
                    f"Valid patterns are: {set(patterns.keys())}"
                )
            self._allowed = list(allowed)
        else:
            self._allowed = list(patterns.keys())
        self._active_pattern: NamePattern | None = None
        super().__init__(parts=[], separator="")

    def regenerate(self) -> None:
        if not hasattr(self, "_named_patterns"):
            return
        self._active_pattern = self._named_patterns[random.choice(self._allowed)]
        self._parts = self._active_pattern.parts
        for part in self._parts:
            part.value = part.generator.generate()

    @property
    def full_name(self) -> str:
        if self._active_pattern is None:
            return ""
        if self._active_pattern.capitalize_slots:
            values = {part.role: capitalize(part.value, {0}) for part in self._parts}
            return self._active_pattern.template.format(**values)
        else:
            values = {part.role: part.value for part in self._parts}
            return capitalize(self._active_pattern.template.format(**values), {0})

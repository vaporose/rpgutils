from __future__ import annotations
from dataclasses import dataclass


@dataclass
class ListEntry:
    """A single entry in a list-based word collection.

    Attributes:
        value: The word or phrase this entry represents.
        context: Semantic domain tags (e.g. 'nautical', 'geographic'). Open-ended.
        grammar: Grammatical role tags. Fixed enum: 'noun', 'adjective', 'prefix', 'suffix'.
    """
    value: str
    context: list[str]
    grammar: list[str]

    @classmethod
    def from_dict(cls, data: dict) -> ListEntry:
        return cls(
            value=data["value"],
            context=data["context"],
            grammar=data["grammar"],
        )


class ListData:
    """
    A loaded word list with inverted indexes for fast tag-based filtering.

    Inverted indexes are built once at load time. Filtering by grammar and/or
    context is O(1) lookup followed by set intersection.

    Attributes:
        entries: The raw list of all entries.
    """

    def __init__(self, entries: list[ListEntry]):
        self.entries = entries
        self._grammar_index: dict[str, list[str]] = {}
        self._context_index: dict[str, list[str]] = {}
        for entry in entries:
            for g in entry.grammar:
                self._grammar_index.setdefault(g, []).append(entry.value)
            for c in entry.context:
                self._context_index.setdefault(c, []).append(entry.value)

    def candidates(
        self,
        grammar: list[str] | None = None,
        context: list[str] | None = None,
    ) -> list[str]:
        """
        Return values matching the given filters.

        When both filters are provided, a value must satisfy both (intersection).
        Within each filter, a value satisfying any one tag qualifies (union).

        Args:
            grammar: Grammatical role tags to match. None means no grammar filter.
            context: Semantic context tags to match. None means no context filter.

        Returns:
            List of matching value strings.
        """
        result: set[str] | None = None

        if grammar:
            matches: set[str] = set()
            for g in grammar:
                matches.update(self._grammar_index.get(g, []))
            result = matches

        if context:
            matches = set()
            for c in context:
                matches.update(self._context_index.get(c, []))
            result = matches if result is None else result & matches

        if result is None:
            return [e.value for e in self.entries]
        return list(result)

    def merge(self, other: ListData) -> ListData:
        """Return a new ListData combining entries from both lists."""
        return ListData(self.entries + other.entries)

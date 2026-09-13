# rpgutils

A Python library of procedural generation utilities for RPG-related projects.

> [!WARNING]
> **This library is under active revision and testing.** The public API is not
> stable — module layout, class names, and call signatures may change without
> notice between commits. Treat anything documented here as provisional, and pin
> a commit if you depend on it.

Requires Python 3.11+. No runtime dependencies.

## Modules

This library is actively being developed, the progress is as follows:

- [x] `rpgutils.names` - A module for generating random names for characters, places, and items. Basic implementation is completed, but more features and options are planned. No dependencies, system agnostic.
- [ ] `rpgutils.characters` - A module for developing random RPG characters, dependent upon the `names` module. System agnostic.
- [ ] `rpgutils.settlement` - A module for generating random settlements, including towns, cities, and villages. System agnostic.
- [ ] `rpgutils.items` - A module for generating random items, including weapons, armor, and magical artifacts. System agnostic.

## `rpgutils.names`

Names are built in two layers. A **generator** produces a single string
component; a **schema** arranges one or more components into a finished name.

```python
from rpgutils.names.generators import ListGenerator
from rpgutils.names.generators.phonetic_generator import PhoneticGenerator
from rpgutils.names.schemas import PersonNameSchema, ShipName

PhoneticGenerator("elvish").generate()      # 'ngaymie'

PersonNameSchema(                            # 'Grirn Kre Grognongem'
    PhoneticGenerator("dwarven"),
    PhoneticGenerator("dwarven"),
    PhoneticGenerator("dwarven"),
)

str(ShipName())                              # 'The Iron Wake'
str(ShipName(allowed=["classic"]))           # 'The Gallant Vengeance'

ListGenerator("english", "nautical", grammar=["adjective"]).generate()   # 'intrepid'
```

### Generators

| Generator | Strategy |
|---|---|
| `PhoneticGenerator(language)` | Builds names syllable by syllable from a language's phoneme profile. |
| `ListGenerator(language, source, ...)` | Draws from a curated word list, filterable by `grammar` (`noun`, `adjective`, `prefix`, `suffix`) and by semantic `context`. Accepts `user_entries` in either `additive` or `override` mode. |
| `Generator` | Abstract base. Subclass it and implement `generate()` to add a strategy. |

All generators accept a `RarityConfig(tiers, decay)`. The default is three tiers —
`common`, `uncommon`, `rare` — with each tier half as likely as the one before it.

### Schemas

| Schema | Produces |
|---|---|
| `NameSchema(parts, separator)` | A custom name from an ordered list of `NamePart(generator, role)`. Each part is reachable as an attribute by its role, e.g. `name.first`. |
| `PersonNameSchema(first, middle, last)` | A three-part personal name. |
| `PatternedNameSchema` / `NamePattern` | A name assembled from template slots, chosen from one of several named patterns. |
| `ShipName(language, allowed)` | A ship name in one of five patterns: `title`, `emblem`, `classic`, `poetic`, `compound`. |

Schemas generate on instantiation. The full name is available via `str()`,
`repr()`, or by calling the instance.

### Bundled data

- **Languages** (`names/data/languages/`) — `dwarven`, `elvish`, `english`,
  `japanese`, `orcish`, `russian`
- **Word lists** (`names/data/lists/`) — `english`: `geographic`, `nautical`,
  `surnames`

All loaded JSON is normalised to NFC Unicode form.

## Development

```bash
uv run --group dev pytest
```

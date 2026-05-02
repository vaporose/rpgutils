from .name_schema import NameSchema, NamePart


class PersonNameSchema(NameSchema):
    """A NameSchema specifically designed for person names, with first and last name parts."""

    def __init__(self, first_generator, middle_generator, last_generator, separator=" "):
        super().__init__(
            parts=[
                NamePart(first_generator, "first"),
                NamePart(middle_generator, "middle"),
                NamePart(last_generator, "last")
            ],
            separator=" ",
        )

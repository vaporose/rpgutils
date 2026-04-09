import json
from random import choice
from abc import ABC, abstractmethod


class Name(ABC):
    """
    A name base class. Currently this is an abstract base class as I had intended to support multiple types of names
    via subclasses.
    """

    def __init__(self, names_to_generate: list):
        """
        :param names_to_generate: A list of templates for each name to generate. Can be a specific template or 'random'.
        """

        self.raw_name = []
        self.get_names(names_to_generate)
        self.nice_name = ' '.join(map(str, self.raw_name))

    @staticmethod
    def _load_reference(thing: str, thing_type: str) -> dict:
        """

        :param thing: Phoneme or Template
        :param thing_type: Only used for templates, specifies the top template layer to be used.
        :return: Dictionary of the extracted phonemes or template
        """
        thing_type = thing_type.title()
        file = '{}.json'.format(thing)  # TODO temporary, update to path to correct files based on settings
        with open(file) as f:
            data = json.load(f)
        thing_list = {x['@Name']: x['Part'] for x in data[thing_type]}
        return thing_list

    def generate(self, template) -> str:
        """
        This performs the main logic in the actual randomization of the name.
        :param template: This is the phoneme template to be used to generate the name.
        :return: Newly generated name
        """
        phonemes = self._load_reference('phonemes', 'phonemes')
        templates = self._load_reference('templates', template)
        random_template: tuple = choice(list(templates.items()))
        # Makes a choice of a template randomly among the templates loaded.
        # The first part of the tuple is the name of the template, the actual pattern is at index 1
        name = ''.join([choice(phonemes[x]) for x in random_template[1]]).title()
        # Pulls out the list of phonemes for each template from the randomly selected template and randomizes it.
        return name

    @abstractmethod
    def get_names(self, names_to_generate: list):
        """
        The logic for exactly how names are generated is handled in this method, overridden by the subclasses.
        :param names_to_generate: A list of templates passed in on initialization.
        """
        pass

    def __repr__(self):
        return self.nice_name


class PersonName(Name):
    """
    Name for a person.

    # TODO expand person names to include additional logic for first, last, middle names
    """
    def get_names(self, names_to_generate: list):
        for template in names_to_generate:
            if template is 'random':
                template = 'Person'  # TODO replace this with something better for randomizing templates
            name = self.generate(template)
            self.raw_name.append(name)


if __name__ == '__main__':
    name = PersonName(['random', 'random', 'random'])
    print(name)

import json
from random import choice


def fetch(thing: str, thing_type: str):
    """
    Generates a dictionary of phonemes or templates, based on required input.
    :param thing: Choice of template or phoneme; which thing to generate
    :param thing_type: This will eventually serve as a category (i.e., ethnicity, genre, person vs place)
    :return: Returns a dictionary with the name of the phoneme/template as key, and a list as the value
    """

    thing_type = thing_type.title()
    file = 'names/{}.json'.format(thing)
    with open(file) as f:
        data = json.load(f)
    thing_list = {x['@Name']: x['Part'] for x in data[thing_type]}
    return thing_list


def gen():
    """
    Fetches current phonemes and templates and generates a name.

    Eventually, this will be expanded so that it generates names limited to specific phonemes or template  parameters.
    :return: Returns a string-based name
    """
    phonemes = fetch('phonemes', 'phonemes')
    templates = fetch('templates', 'person')
    random_template = choice(list(templates.items()))
    name = ''.join([choice(phonemes[x]) for x in random_template[1]]).title()
    return name


def main():
    print(gen())


if __name__ == '__main__':
    main()

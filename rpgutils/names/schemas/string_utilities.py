
def capitalize(string: str, characters_to_capitalize: set[int]) -> str:
    """
    Capitalizes characters in a string based on their indices.

    Args:
        string: The input string to capitalize.
        characters_to_capitalize: A set of integer indices indicating which characters to capitalize.
    Returns:
        The capitalized string.
    """
    if not string:
        return string
    chars = list(string)
    for index in characters_to_capitalize:
        chars[index] = chars[index].upper()
    return "".join(chars)

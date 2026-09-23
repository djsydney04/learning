"""Run from the project root: python -m labs.01_python

Experiment: change MESSAGE to "taco" and predict every printed value.
Then add a function that counts how many times a character occurs.
"""

MESSAGE = "cat"


def encode(text, char_to_id):
    """Turn a string into a list of integer IDs."""
    ids = []
    for character in text:
        ids.append(char_to_id[character])
    return ids


class Vocabulary:
    """Keep a vocabulary and its conversion functions together."""

    def __init__(self, text):
        # set removes duplicates; sorted gives a stable alphabetical order.
        self.characters = sorted(set(text))
        self.char_to_id = {}
        for index, character in enumerate(self.characters):
            self.char_to_id[character] = index

    def encode(self, text):
        return encode(text, self.char_to_id)

    def decode(self, ids):
        characters = []
        for token_id in ids:
            characters.append(self.characters[token_id])
        return "".join(characters)


def main():
    vocabulary = Vocabulary(MESSAGE)
    ids = vocabulary.encode(MESSAGE)
    print("message:", MESSAGE)
    print("first character:", MESSAGE[0])
    print("all except first:", MESSAGE[1:])
    print("characters:", vocabulary.characters)
    print("character -> ID:", vocabulary.char_to_id)
    print("IDs:", ids)
    print("decoded:", vocabulary.decode(ids))
    print("integer versus float:", type(3).__name__, type(3.0).__name__)

    # Assertions turn expectations into executable checks.
    assert vocabulary.decode(ids) == MESSAGE
    assert len(ids) == len(MESSAGE)
    if MESSAGE == "cat":
        assert ids == [1, 0, 2]
    print("All Python checks passed.")


# This is true when Python runs this file as a program. Importing its classes
# from another module will not run the demonstration.
if __name__ == "__main__":
    main()

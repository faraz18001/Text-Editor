class Node:
    def __init__(self):
        self.children = {}
        self.end_of_word = False

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str):
        current = self.root
        for character in word:
            if character not in current.children:
                current.children[character] = Node()
            current = current.children[character]
        current.end_of_word = True

    def search(self, word):
        current = self.root
        for character in word:
            if character not in current.children:
                return False
            current = current.children[character]  # This line should be INSIDE the loop
        return current.end_of_word

    def starts_with(self, prefix: str):
        current = self.root
        for character in prefix:
            if character not in current.children:  # Fixed logic and removed parentheses
                return False
            current = current.children[character]
        return True

END_OF_WORD = '*'

def create_trie():
    """
    Creates an empty trie, which is just an empty dictionary.
    This dictionary represents the root node.
    """
    return {}

def insert(trie: dict, word: str):
    """
    Inserts a word into the trie.
    The 'trie' argument is the root dictionary.
    """
    current_node = trie
    for character in word:
        if character not in current_node:
            current_node[character] = {}
        current_node = current_node[character]

    current_node[END_OF_WORD] = True

def search(trie: dict, word: str) -> bool:
    """
    Searches for a complete word in the trie.
    Returns True if the word exists, False otherwise.
    """
    current_node = trie
    for character in word:
        if character not in current_node:
            return False
        current_node = current_node[character]

    return END_OF_WORD in current_node

def starts_with(trie: dict, prefix: str) -> bool:
    """
    Checks if there is any word in the trie that starts with the given prefix.
    """
    current_node = trie
    for character in prefix:
        if character not in current_node:
            return False
        current_node = current_node[character]

    return True

trie = create_trie()

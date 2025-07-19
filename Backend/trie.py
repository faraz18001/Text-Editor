from nltk.corpus import words
import nltk
nltk.download('words')
END_OF_WORD = '*'

def create_trie():

    return {}

def insert(trie: dict, word: str):

    current_node = trie
    for character in word:
        if character not in current_node:
            current_node[character] = {}
        current_node = current_node[character]

    current_node[END_OF_WORD] = True

def search(trie: dict, word: str) -> bool:

    current_node = trie
    for character in word:
        if character not in current_node:
            return False
        current_node = current_node[character]

    return END_OF_WORD in current_node

def starts_with(trie: dict, prefix: str) -> bool:

    current_node = trie
    for character in prefix:
        if character not in current_node:
            return False
        current_node = current_node[character]

    return True


#
#
                    ##--Training and Inserting Words inside the trie----##



word_list = words.words()
def train_trie(trie: dict, word_list:list):
    # Runtime Complexity: O(N * M) where N is the number of words and M is the average length of words
    # Space Complexity: O(N * M) for storing all words in the trie structure
    for word in word_list:
        insert(trie, word)

    return trie



trie = train_trie(create_trie(), word_list)


"""print(f"Number of words in trie: {len(word_list)}")
print(f"Search for 'hello': {search(trie, 'hello')}")
print(f"Search for 'world': {search(trie, 'world')}")
print(f"Search for 'python': {search(trie, 'python')}")
print(f"Search for 'nonexistentword': {search(trie, 'nonexistentword')}")
print(f"Starts with 'hel': {starts_with(trie, 'hel')}")
print(f"Starts with 'wor': {starts_with(trie, 'wor')}")
print(f"Starts with 'xyz': {starts_with(trie, 'xyz')}")"""

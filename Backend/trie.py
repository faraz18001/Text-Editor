from enum import auto
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

    def collection_completions(node,current_word,suggestions,max_suggestions):
        if len(suggestions)>=max_suggestions:
            return

        if END_OF_WORD in node:
            suggestions.append(current_word)

        for char child_node in node.items():
            if char!=END_OF_WORD:
                collect_completion=child(current_node+char,suggestion,max)


#
#
                    ##--Training and Inserting Words inside the trie----##



word_list = words.words()
def train_trie(trie: dict, word_list:list):

    for word in word_list:
        insert(trie, word)

    return trie

trie = train_trie(create_trie(), word_list)

###Auto Complete Fucntion##

def autocomplete(trie: dict, prefix: str, max_suggestions: int = 10):
    suggestions = []

    current_node = trie
    for char in prefix:
        if char not in current_node:
            return suggestions
        current_node = current_node[char]


    def collect_completions(node, current_word, suggestions, max_suggestions):
        if len(suggestions) >= max_suggestions:
            return

        if END_OF_WORD in node:
            suggestions.append(current_word)

        for char, child_node in node.items():
            if char != END_OF_WORD:
                collect_completions(child_node, current_word + char, suggestions, max_suggestions)

    collect_completions(current_node, prefix, suggestions, max_suggestions)
    return suggestions

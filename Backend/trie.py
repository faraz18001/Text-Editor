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
word_list = words.words()#this has around 27500 words



def train_trie(trie: dict, word_list:list):

    for word in word_list:
        insert(trie, word)

    return trie



trie = train_trie(create_trie(), word_list)


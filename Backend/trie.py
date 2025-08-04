# ==============================================================================
# I. IMPORTS AND INITIAL SETUP
# ==============================================================================

import json
import nltk
from nltk.corpus import words
from emoji_data import word_to_emoji

# Download necessary NLTK data
nltk.download("words")

# Define a constant to mark the end of a word in the Trie
END_OF_WORD = "*"


# ==============================================================================
# II. CORE TRIE DATA STRUCTURE IMPLEMENTATION
#
# These are the fundamental functions for creating and interacting with a
# Trie data structure.
# ==============================================================================

def create_trie():
    return {}


def insert(trie: dict, word: str):
    current_node = trie
    for character in word.lower():
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


def get_node_at_prefix(trie: dict, prefix: str):
    current_node = trie
    for character in prefix:
        if character not in current_node:
            return None
        current_node = current_node[character]
    return current_node


# ==============================================================================
# III. GENERAL-PURPOSE WORD AUTOCOMPLETE & TRAINING
#
# Functions that use the core Trie to provide word suggestions and to train
# the Trie from a list of words.
# ==============================================================================

def get_all_words_from_node(node: dict, prefix: str, max_suggestions: int = 10):
    suggestions = []

    def collect_words(current_node, current_word):
        if len(suggestions) >= max_suggestions:
            return

        if END_OF_WORD in current_node:
            suggestions.append(current_word)

        for char, child_node in current_node.items():
            if char != END_OF_WORD and len(suggestions) < max_suggestions:
                collect_words(child_node, current_word + char)

    collect_words(node, prefix)
    return suggestions


def autocomplete(trie: dict, prefix: str, max_suggestions: int = 10):
    suggestions = []
    prefix_lower = prefix.lower()
    if not starts_with(trie, prefix_lower):
        return suggestions

    prefix_node = get_node_at_prefix(trie, prefix_lower)
    if prefix_node is None:
        return suggestions

    suggestions = get_all_words_from_node(prefix_node, prefix_lower, max_suggestions)
    return suggestions


def train_trie(trie: dict, word_list: list):
    for word in word_list:
        insert(trie, word)
    return trie


# ==============================================================================
# IV. EMOJI INTEGRATION FUNCTIONS
#
# Specialized functions to insert, search, and suggest words linked to emojis.
# The end-of-word marker stores the emoji string instead of True.
# ==============================================================================

def insert_emoji(trie: dict, word: str, emoji: str):
    current_node = trie
    for character in word.lower():
        if character not in current_node:
            current_node[character] = {}
        current_node = current_node[character]
    current_node[END_OF_WORD] = emoji


def search_emoji(trie: dict, word: str) -> str:
    current_node = trie
    for character in word.lower():
        if character not in current_node:
            return ''
        current_node = current_node[character]
    if END_OF_WORD in current_node and isinstance(current_node[END_OF_WORD], str):
        return current_node[END_OF_WORD]
    else:
        return ''


def autocomplete_emoji(trie: dict, prefix: str, max_suggestions: int = 10):
    suggestions = []
    prefix_lower = prefix.lower()
    prefix_node = get_node_at_prefix(trie, prefix_lower)
    if prefix_node is None:
        return suggestions

    def collect_emoji_words(current_node, current_word):
        if len(suggestions) >= max_suggestions:
            return
        if END_OF_WORD in current_node:
            emoji = current_node[END_OF_WORD]
            suggestions.append((current_word, emoji))
        for char, child_node in current_node.items():
            if char != END_OF_WORD and len(suggestions) < max_suggestions:
                collect_emoji_words(child_node, current_word + char)

    collect_emoji_words(prefix_node, prefix_lower)
    return suggestions


def train_emoji_trie(trie: dict, emoji_mappings: dict):
    for word, emoji in emoji_mappings.items():
        insert_emoji(trie, word, emoji)
    return trie


# ==============================================================================
# V. PUNCTUATION ANALYSIS FUNCTIONS
#
# Functions to identify and name punctuation characters within text using a
# simplified Trie.
# ==============================================================================

def insert_punctuation(trie: dict, char: str, name: str):
    current_node = trie
    if char not in current_node:
        current_node[char] = {}
    current_node = current_node[char]
    current_node[END_OF_WORD] = name


def search_punctuation(trie: dict, char: str) -> str:
    if char in trie and END_OF_WORD in trie[char]:
        return trie[char][END_OF_WORD]
    return ''


def train_punctuation_trie(trie: dict):
    punctuation_data = {
        '.': 'period', ',': 'comma', '!': 'exclamation', '?': 'question',
        ';': 'semicolon', ':': 'colon', "'": 'apostrophe', '"': 'quotation',
        '-': 'hyphen', '(': 'left_parenthesis', ')': 'right_parenthesis',
    }
    for char, name in punctuation_data.items():
        insert_punctuation(trie, char, name)
    return trie


def analyze_sentence_punctuation(punct_trie: dict, sentence: str):
    found_punctuation = []
    for char in sentence:
        punct_name = search_punctuation(punct_trie, char)
        if punct_name:
            found_punctuation.append((char, punct_name))
    return found_punctuation


# ==============================================================================
# VI. ABBREVIATION EXPANSION FUNCTIONS
#
# Functions to load, search for, and expand abbreviations within a sentence.
# The end-of-word marker stores the expanded form of the abbreviation.
# ==============================================================================

def load_abbreviations_from_json(filepath: str) -> dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def search_and_expand(trie: dict, word: str) -> str:

    current_node = trie
    lookup_word = word.lower().strip('.,!?;:"\'()[]{}')

    for character in lookup_word:
        if character not in current_node:
            return word
        current_node = current_node[character]

    if END_OF_WORD in current_node:
        value = current_node[END_OF_WORD]
        if isinstance(value, str):
            return value
    return word


def expand_abbreviations_in_sentence(trie: dict, sentence: str) -> str:
    words_in_sentence = sentence.split()
    expanded_words = []
    for w in words_in_sentence:
        expanded_words.append(search_and_expand(trie, w))
    return " ".join(expanded_words)

# ==============================================================================
# 1. IMPORTS AND SETUP
# ==============================================================================

from nltk.corpus import words
import nltk
from emoji_data import word_to_emoji


# Download the necessary NLTK data.
# Note: The original code downloads this every time.
nltk.download("words")

# Global constant for marking the end of a word in the Trie.
END_OF_WORD = "*"


# ==============================================================================
# 2. GENERIC TRIE CREATION
# ==============================================================================

def create_trie():
    """
    1.Simpled Data Structure Implementation using DICT'S
    2.Just like the binary search tree and graph implementation in the labs
    """
    return {}


# ==============================================================================
# 3. STANDARD WORD TRIE IMPLEMENTATION
#    (Handles a standard dictionary of words from NLTK)
# ==============================================================================

def insert(trie: dict, word: str):
    """
    1.First get the root of the tree.
    2.Now traverse the each letter of the word
    3. And now check if that word exists in the root aka the current_node.
    4.If it doesn't for that specific word create another node nested there and put it there
    5.If it does already tehn just move the pointer downward
    6.now we have to mark the end of the word, to make sure we don't go on forver
    """
    current_node = trie
    for character in word.lower():
        if character not in current_node:
            current_node[character] = {}
        current_node = current_node[character]
    current_node[END_OF_WORD] = True


def search(trie: dict, word: str) -> bool:
    """
    1.again grab the root node.
    2. now traverse the words characters and check if the current character that you are iterating over
    3. is inside the current node, if not even a single character which the starts from return False.
    4.else move down, one by one check each character and once you have found all the letters inside ther tree
    5.you must have hit the end of the word tombstone, so return True that means the word exists.
    """
    current_node = trie
    for character in word:
        if character not in current_node:
            return False
        current_node = current_node[character]
    return END_OF_WORD in current_node


def starts_with(trie: dict, prefix: str) -> bool:
    """
    1.grab the root node, of the trei
    2. traverse on the prefix string, if the starting letter of the prefix doesn't exists inside the current node
    3.return false
    4.else move 1 level down in the tree and repeat the process, you have found the word which has the same prefix.
    5.which you have passed down the function return True
    """
    current_node = trie
    for character in prefix:
        if character not in current_node:
            return False
        current_node = current_node[character]
    return True


def get_node_at_prefix(trie: dict, prefix: str):
    """
    This function is sam has starts with
    but just it has one statement change
    that it returns the node if it exists
    """
    current_node = trie
    for character in prefix:
        if character not in current_node:
            return None
        current_node = current_node[character]
    return current_node


def get_all_words_from_node(node: dict, prefix: str, max_suggestions: int = 10):
    """
    1.okay this function uses recursin specifically the collect words functions
    2.the base case for this function is that when ever we our suggestions list hit the lenght of max_suggestion.
    3.we return back to the function which called the collected words functions.
    4.
    """
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
    """
    Autocomplete function that uses existing helper functions:
    1. first use starts_with() to check if prefix exists
    2. use get_node_at_prefix() to navigate to the prefix location
    3. use get_all_words_from_node() to collect completions
    """
    suggestions = []

    if not starts_with(trie, prefix):
        return suggestions

    prefix_node = get_node_at_prefix(trie, prefix)
    if prefix_node is None:
        return suggestions

    suggestions = get_all_words_from_node(prefix_node, prefix, max_suggestions)
    return suggestions


def train_trie(trie: dict, word_list: list):
    """
    1.first we pass the wordlist from nltk library
    2. now here we selected each word one by one form the 87500 word list.
    3.then we call the insert function and pass every single word one by one.
    4.now our trie is trained we just return it
    """
    for word in word_list:
        insert(trie, word)
    return trie


# ==============================================================================
# 4. EMOJI TRIE IMPLEMENTATION
#    (Handles a dictionary of word-to-emoji mappings)
# ==============================================================================

def insert_emoji(trie: dict, word: str, emoji: str):
    """
    1.this function is the same as exact the insert on.
    2.but just there is difference of 1 line which is that we are
    3.checking if the end of the word is a emoji.
    """
    current_node = trie
    for character in word.lower():
        if character not in current_node:
            current_node[character] = {}
        current_node = current_node[character]
    current_node[END_OF_WORD] = emoji


def search_emoji(trie: dict, word: str) -> bool:
    current_node = trie
    for character in word.lower():
        if character not in current_node:
            return ''
        current_node = current_node[character]
    if END_OF_WORD in current_node:
        return current_node[END_OF_WORD]
    else:
        return ''


def starts_with_emoji(trie: dict, prefix: str) -> bool:
    current_node = trie
    for character in prefix.lower():
        if character not in current_node:
            return False
        current_node = current_node[character]
    return True


def get_node_at_prefix_emoji(trie: dict, prefix: str):
    current_node = trie
    for character in prefix.lower():
        if character not in current_node:
            return None
        current_node = current_node[character]
    return current_node


def get_all_emojis_from_node(node: dict, prefix: str, max_suggestions: int = 10):
    suggestions = []

    def collect_emoji_words(current_node, current_word):
        if len(suggestions) >= max_suggestions:
            return

        if END_OF_WORD in current_node:
            emoji = current_node[END_OF_WORD]
            suggestions.append((current_word, emoji))

        for char, child_node in current_node.items():
            if char != END_OF_WORD and len(suggestions) < max_suggestions:
                collect_emoji_words(child_node, current_word + char)

    collect_emoji_words(node, prefix)
    return suggestions


def autocomplete_emoji(trie: dict, prefix: str, max_suggestions: int = 10):
    suggestions = []

    if not starts_with_emoji(trie, prefix):
        return suggestions

    prefix_node = get_node_at_prefix_emoji(trie, prefix)
    if prefix_node is None:
        return suggestions

    suggestions = get_all_emojis_from_node(prefix_node, prefix.lower(), max_suggestions)
    return suggestions


def train_emoji_trie(trie: dict, emoji_mappings: dict):
    for word, emoji in emoji_mappings.items():
        insert_emoji(trie, word, emoji)
    return trie


# ==============================================================================
# 5. PUNCTUATION TRIE IMPLEMENTATION (NEW ADDITION)
#    (Handles punctuation marks with their names/descriptions)
# ==============================================================================

def insert_punctuation(trie: dict, char: str, name: str):

    current_node = trie
    # For punctuation, we use the character itself as the path
    if char not in current_node:
        current_node[char] = {}
    current_node = current_node[char]
    current_node[END_OF_WORD] = name


def search_punctuation(trie: dict, char: str) -> str:
    """
    Search for a punctuation character and return its name
    """
    current_node = trie
    if char not in current_node:
        return ''
    current_node = current_node[char]
    if END_OF_WORD in current_node:
        return current_node[END_OF_WORD]
    else:
        return ''


def is_punctuation(trie: dict, char: str) -> bool:
    """
    Check if a character is a known punctuation mark
    """
    return search_punctuation(trie, char) != ''


def train_punctuation_trie(trie: dict):
    """
    Train the punctuation trie with common punctuation marks
    """
    punctuation_data = {
        '.': 'period',
        ',': 'comma',
        '!': 'exclamation',
        '?': 'question',
        ';': 'semicolon',
        ':': 'colon',
        "'": 'apostrophe',
        '"': 'quotation',
        '-': 'hyphen',
        '(': 'left_parenthesis',
        ')': 'right_parenthesis',
        '[': 'left_bracket',
        ']': 'right_bracket',
        '{': 'left_brace',
        '}': 'right_brace'
    }

    for char, name in punctuation_data.items():
        insert_punctuation(trie, char, name)
    return trie


def analyze_sentence_punctuation(punct_trie: dict, sentence: str):
    """
    Analyze a sentence and return all punctuation found with their names
    """
    found_punctuation = []
    for char in sentence:
        punct_name = search_punctuation(punct_trie, char)
        if punct_name is not None:
            found_punctuation.append((char, punct_name))
    return found_punctuation

# ==============================================================================
# 7. ABBREVIATION EXPANSION (INTEGRATED INTO STANDARD TRIE)
# ==============================================================================

def search_and_expand(trie: dict, word: str) -> str:
    """
    Searches for a word in the trie.
    - If the word is an abbreviation, returns its expansion.
    - If the word is a standard word, returns the word itself.
    - If the word is not found, returns the word itself.

    This function handles both regular words (marked with True) and
    abbreviations (marked with their string expansion).
    """
    current_node = trie
    # Clean the word of potential surrounding punctuation for a better lookup
    # and convert to lowercase as the trie is case-insensitive.
    lookup_word = word.lower().strip('.,!?;:"\'()[]{}')

    for character in lookup_word:
        if character not in current_node:
            return word  # Word not in trie, return original
        current_node = current_node[character]

    if END_OF_WORD in current_node:
        value = current_node[END_OF_WORD]
        # If the value is a string, it's an expansion.
        if isinstance(value, str):
            return value
        # Otherwise, it's a regular word (value is True), so return original.
        else:
            return word
    else:
        # It's a prefix but not a complete word in our trie.
        return word


def expand_abbreviations_in_sentence(trie: dict, sentence: str) -> str:
    """
    Processes a sentence, expanding any known abbreviations found in the trie.
    """
    words_in_sentence = sentence.split()

    expanded_words = []
    for w in words_in_sentence:
        expanded_words.append(search_and_expand(trie, w))

    return " ".join(expanded_words)







# ==============================================================================
# 6. DATA LOADING, TRIE TRAINING, AND EXECUTION
# ==============================================================================


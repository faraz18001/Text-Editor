# ==============================================================================
# 1. IMPORTS AND SETUP
# ==============================================================================
import tkinter as tk
from tkinter import ttk
import nltk
from nltk.corpus import words
from emoji_data import word_to_emoji
import ctypes
import os

try:
    from PIL import Image, ImageTk
except ImportError:
    print("ERROR: The Pillow library is not found. Please install it: pip install Pillow")
    exit()

# Download NLTK data if necessary
try:
    words.ensure_loaded()
except LookupError:
    print("Downloading NLTK 'words' corpus...")
    nltk.download("words")

END_OF_WORD = "*"

# ==============================================================================
# 2. TRIE LOGIC (Already Procedural - No Changes Needed)
# ==============================================================================
def create_trie(): return {}
def insert(trie, word):
    node = trie
    for char in word.lower():
        if char not in node: node[char] = {}
        node = node[char]
    node[END_OF_WORD] = True
def get_node_at_prefix(trie, prefix):
    node = trie
    for char in prefix:
        if char not in node: return None
        node = node[char]
    return node
def get_all_words_from_node(node, prefix, max_suggestions=10):
    suggestions = []
    def collect(current_node, current_word):
        if len(suggestions) >= max_suggestions: return
        if END_OF_WORD in current_node: suggestions.append(current_word)
        for char, child in sorted(current_node.items()):
            if char != END_OF_WORD and len(suggestions) < max_suggestions:
                collect(child, current_word + char)
    if node: collect(node, prefix)
    return suggestions
def autocomplete(trie, prefix, max_suggestions=10):
    prefix_lower = prefix.lower()
    node = get_node_at_prefix(trie, prefix_lower)
    return get_all_words_from_node(node, prefix_lower, max_suggestions) if node else []
def train_trie(trie, word_list):
    for word in word_list:
        if word.isalpha(): insert(trie, word)
    return trie
def insert_emoji(trie, word, emoji):
    node = trie
    for char in word.lower():
        if char not in node: node[char] = {}
        node = node[char]
    if END_OF_WORD not in node: node[END_OF_WORD] = []
    node[END_OF_WORD].append(emoji)
def get_all_emojis_from_node(node, prefix, max_suggestions=10):
    suggestions = []
    def collect(current_node, current_word):
        if len(suggestions) >= max_suggestions: return
        if END_OF_WORD in current_node:
            for emoji in current_node[END_OF_WORD]:
                suggestions.append((current_word, emoji))
                if len(suggestions) >= max_suggestions: return
        for char, child in sorted(current_node.items()):
            if char != END_OF_WORD and len(suggestions) < max_suggestions:
                collect(child, current_word + char)
    if node: collect(node, prefix)
    return suggestions
def autocomplete_emoji(trie, prefix, max_suggestions=10):
    prefix_lower = prefix.lower()
    node = get_node_at_prefix(trie, prefix_lower)
    return get_all_emojis_from_node(node, prefix_lower, max_suggestions) if node else []
def train_emoji_trie(trie, emoji_mappings):
    for word, emoji in emoji_mappings.items():
        clean_word = word.replace(":", "").replace("_", " ").strip()
        if clean_word: insert_emoji(trie, clean_word, emoji)
    return trie

# ==============================================================================
# 3. GLOBAL VARIABLES FOR APPLICATION STATE
# ==============================================================================
# These variables replace the 'self' attributes from the OOP version
word_trie = {}
emoji_trie = {}
suggestion_list_visible = False
current_prefix = ""
emoji_image_cache = {}
emoji_references = [] # Prevents garbage collection of images

# GUI Widgets will be assigned here later
root = None
text_editor = None
suggestion_listbox = None
mode = None

# ==============================================================================
# 4. GUI HELPER FUNCTIONS
# ==============================================================================

def get_emoji_image(emoji_char):
    """Loads and caches PhotoImage objects for emojis."""
    global emoji_image_cache
    if emoji_char in emoji_image_cache:
        return emoji_image_cache[emoji_char]

    codepoint = '-'.join(f'{ord(c):x}' for c in emoji_char)
    image_path = os.path.join('emojis', f'{codepoint}.png')

    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return None

    try:
        img = Image.open(image_path).convert("RGBA")
        font_size_str = text_editor.cget("font").split()[-1]
        size = int(font_size_str) + 4
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        photo_img = ImageTk.PhotoImage(img)
        emoji_image_cache[emoji_char] = photo_img
        return photo_img
    except Exception as e:
        print(f"Error loading emoji {emoji_char}: {e}")
        return None

def complete_word(event):
    """Insert the selected suggestion into the text editor."""
    global emoji_references
    if not suggestion_listbox.curselection():
        hide_suggestions(refocus_editor=True)
        return "break"

    selected_text = suggestion_listbox.get(suggestion_listbox.curselection())
    prefix_start_index = text_editor.index(f"insert - {len(current_prefix)} chars")
    text_editor.delete(prefix_start_index, tk.INSERT)

    parts = selected_text.split()
    if len(parts) > 1 and mode.get() == 'emoji':
        word, emoji_char = parts[0], parts[1]
        text_editor.insert(tk.INSERT, word)
        emoji_image = get_emoji_image(emoji_char)
        if emoji_image:
            emoji_references.append(emoji_image)
            text_editor.image_create(tk.INSERT, image=emoji_image, padx=2)
        else:
            text_editor.insert(tk.INSERT, emoji_char)
        text_editor.insert(tk.INSERT, " ")
    else:
        text_editor.insert(tk.INSERT, selected_text + " ")

    hide_suggestions(refocus_editor=True)
    return "break"

def on_key_release(event):
    """Handle key releases to show/hide/update suggestions."""
    global current_prefix
    if event.keysym in ("Up", "Left", "Right", "BackSpace", "space", "Return", "period", "comma", "Escape", "Down"):
        hide_suggestions()
        return

    cursor_pos = text_editor.index(tk.INSERT)
    line_start = text_editor.index(f"{cursor_pos} linestart")
    text_before_cursor = text_editor.get(line_start, cursor_pos)
    parts = text_before_cursor.split(' ')

    current_prefix = parts[-1] if parts else ""
    if not current_prefix:
        hide_suggestions()
        return

    if mode.get() == "word":
        suggestions = autocomplete(word_trie, current_prefix)
    else:
        raw_suggestions = autocomplete_emoji(emoji_trie, current_prefix, 15)
        suggestions = [f"{word} {emoji}" for word, emoji in raw_suggestions]

    if suggestions:
        show_suggestions(suggestions)
    else:
        hide_suggestions()

def navigate_to_suggestions(event):
    """Move focus to the suggestion listbox when Down arrow is pressed."""
    if suggestion_list_visible:
        suggestion_listbox.focus_set()
        suggestion_listbox.selection_set(0)
        return "break"

def show_suggestions(suggestions):
    """Display the suggestion listbox below the cursor."""
    global suggestion_list_visible
    suggestion_listbox.delete(0, tk.END)
    for item in suggestions:
        suggestion_listbox.insert(tk.END, item)
    x, y, _, height = text_editor.bbox(tk.INSERT)
    suggestion_listbox.place(x=x, y=y + height)
    suggestion_listbox.config(height=min(len(suggestions), 8))
    suggestion_list_visible = True

def hide_suggestions(refocus_editor=False):
    """Hide the suggestion listbox."""
    global suggestion_list_visible
    suggestion_listbox.place_forget()
    suggestion_list_visible = False
    if refocus_editor:
        text_editor.focus_set()

# ==============================================================================
# 5. MAIN EXECUTION BLOCK
# ==============================================================================
if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    print("Loading and training data...")
    word_list_data = words.words()
    word_trie = train_trie(create_trie(), word_list_data)
    emoji_trie = train_emoji_trie(create_trie(), word_to_emoji)
    print("Training complete.")

    print("Launching GUI...")
    root = tk.Tk()
    root.title("Autocomplete Text Editor (Procedural)")
    root.geometry("700x500")

    style = ttk.Style(root)
    try:
        style.theme_use("vista")
    except tk.TclError:
        print("Vista theme not available, using default.")

    # --- Create Widgets and assign to global variables ---
    control_frame = ttk.Frame(root)
    control_frame.pack(fill=tk.X, padx=5, pady=5)

    mode = tk.StringVar(value="word")

    ttk.Label(control_frame, text="Autocomplete Mode:").pack(side=tk.LEFT, padx=(0, 10))
    ttk.Radiobutton(control_frame, text="Words", variable=mode, value="word").pack(side=tk.LEFT)
    ttk.Radiobutton(control_frame, text="Emojis", variable=mode, value="emoji").pack(side=tk.LEFT)

    text_editor = tk.Text(root, font=("Segoe UI", 12), undo=True, wrap=tk.WORD)
    text_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
    text_editor.focus_set()

    suggestion_listbox = tk.Listbox(text_editor, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)

    # --- Bind Events to Functions ---
    text_editor.bind("<KeyRelease>", on_key_release)
    text_editor.bind("<Down>", navigate_to_suggestions)
    suggestion_listbox.bind("<Return>", complete_word)
    suggestion_listbox.bind("<Tab>", complete_word)
    suggestion_listbox.bind("<Escape>", lambda e: hide_suggestions(refocus_editor=True))
    suggestion_listbox.bind("<FocusOut>", lambda e: hide_suggestions(refocus_editor=False))

    # --- Start the Application ---
    root.mainloop()

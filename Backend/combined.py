# ==============================================================================
# I. IMPORTS
# ==============================================================================

import os
import json
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox, ttk
from tkinter import font as tkFont
from tkinter import colorchooser
from PIL import Image, ImageTk
from PIL.Image import Resampling

import trie


# ==============================================================================
# II. INITIAL DATA TRAINING
#
# Load and train all necessary data structures (Tries) at startup.
# ==============================================================================

print("Training all data tries. This may take a moment...")
main_trie = trie.train_trie(trie.create_trie(), trie.words.words())

emoji_trie = trie.train_emoji_trie(trie.create_trie(), trie.word_to_emoji)

punctuation_trie = trie.train_punctuation_trie(trie.create_trie())

abbreviation_data = trie.load_abbreviations_from_json("abbreviations.json")
for abbr, expansion in abbreviation_data.items():
    trie.insert_emoji(main_trie, abbr, expansion)
print("All Tries Ready.")


# ==============================================================================
# III. MAIN WINDOW AND GLOBAL VARIABLES
# ==============================================================================

#  main window
master = Tk()
master.title("Untitled* - Script Editor")
master.geometry("800x600")
master.resizable(True, True)
master.minsize(800, 600)

# --- GLOBAL VARIABLES ---
file_name = ""
autocomplete_window = None
current_font_family = "Cascada Mono"
current_font_size = 12


# ==============================================================================
# IV. AUTOCOMPLETE AND ANALYSIS FUNCTIONS
#
# Logic for handling autocomplete suggestions and other text analysis tools.
# ==============================================================================

def on_autocomplete_select(event):
    global autocomplete_window
    widget = event.widget
    selection_index = widget.curselection()
    if selection_index:
        value = widget.get(selection_index[0])
        # Handle emoji suggestions which have two parts
        if len(value.split()) > 1:
            value = value.split()[-1]
        start_index = text.index("insert-1c wordstart")
        end_index = text.index("insert")
        text.delete(start_index, end_index)
        text.insert(start_index, value)
    if autocomplete_window:
        autocomplete_window.destroy()
        autocomplete_window = None


def handle_autocomplete(event):
    global autocomplete_window
    if autocomplete_window:
        autocomplete_window.destroy()
        autocomplete_window = None

    start = text.index("insert-1c wordstart")
    end = text.index("insert")
    prefix = text.get(start, end)
    if len(prefix) < 2:
        return

    word_suggestions = trie.autocomplete(main_trie, prefix)
    emoji_suggestions = trie.autocomplete_emoji(emoji_trie, prefix)
    all_suggestions = word_suggestions + emoji_suggestions
    if not all_suggestions:
        return

    autocomplete_window = Toplevel(master)
    autocomplete_window.wm_overrideredirect(True)
    autocomplete_window.configure(bg='white', relief='solid', bd=1)

    try:
        bbox = text.bbox(INSERT)
        if bbox:
            x, y, _, height = bbox
            abs_x = text.winfo_rootx() + x
            abs_y = text.winfo_rooty() + y + height + 5
            autocomplete_window.geometry(f"+{abs_x}+{abs_y}")
        else:
            autocomplete_window.geometry(f"+{master.winfo_x() + 100}+{master.winfo_y() + 100}")
    except:
        autocomplete_window.geometry(f"+{master.winfo_x() + 100}+{master.winfo_y() + 100}")

    listbox = Listbox(autocomplete_window, height=min(len(all_suggestions), 5))
    listbox.pack()

    for suggestion in all_suggestions:
        if isinstance(suggestion, tuple):
            display_text = f"{suggestion[0]} {suggestion[1]}"
            listbox.insert(END, display_text)
        else:
            listbox.insert(END, suggestion)

    listbox.bind("<<ListboxSelect>>", on_autocomplete_select)


def show_punctuation_analysis():

    content = text.get("1.0", END)
    analysis = trie.analyze_sentence_punctuation(punctuation_trie, content)
    if not analysis:
        messagebox.showinfo("Punctuation Analysis", "No standard punctuation found.")
        return
    result_str = "Found Punctuation:\n\n"
    for char, name in analysis:
        result_str += f"'{char}' -> {name}\n"
    messagebox.showinfo("Punctuation Analysis", result_str)


def run_abbreviation_expansion():
    content = text.get("1.0", END)
    expanded_content = trie.expand_abbreviations_in_sentence(main_trie, content)
    text.delete("1.0", END)
    text.insert("1.0", expanded_content)
    messagebox.showinfo("Expansion Complete", "Abbreviations have been expanded in the text.")


# ==============================================================================
# V. FILE AND EDITING FUNCTIONS
#
# Standard text editor operations like New, Open, Save, Cut, Copy, Paste.
# ==============================================================================

def new():
    global file_name
    if messagebox.askquestion(title="Save File", message="Would you like to save this file?") == 'yes':
        save()
    text.delete("1.0", END)
    file_name = ""
    master.title("Untitled* - Script Editor")


def open_file():
    global file_name
    if messagebox.askquestion(title="Save File", message="Would you like to save before opening?") == 'yes':
        save()
    path = filedialog.askopenfilename()
    if path:
        file_name = path
        master.title(f"{os.path.basename(file_name)} - Script Editor")
        text.delete("1.0", END)
        with open(file_name, 'r') as file:
            text.insert(INSERT, file.read())


def save():
    global file_name
    if not file_name:
        path = filedialog.asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt")
        if not path:
            return
        file_name = path
    with open(file_name, 'w') as write:
        write.write(text.get("1.0", END))
    master.title(f"{os.path.basename(file_name)} - Script Editor")


def close():
    if messagebox.askquestion(title="Save File", message="Would you like to save before quitting?") == 'yes':
        save()
    master.quit()


def cut(): master.event_generate("<<Cut>>")
def copy(): master.event_generate("<<Copy>>")
def paste(): master.event_generate("<<Paste>>")
def select_all(): text.tag_add(SEL, "1.0", END); return "break"
def undo(): text.edit_undo()
def redo(): text.edit_redo()


# ==============================================================================
# VI. TEXT FORMATTING FUNCTIONS
#
# Functions to apply various styles and formats to the selected text.
# ==============================================================================

def change_font_color():
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code and color_code[1]:
        color_tag = f"color{color_code[1].replace('#', '')}"
        text.tag_config(color_tag, foreground=color_code[1])
        if text.tag_ranges("sel"):
            text.tag_add(color_tag, "sel.first", "sel.last")


def clear_formatting():
    if text.tag_ranges("sel"):
        tags_to_remove = ["bold", "italic", "underline", "overstrike", "blockquote", "code"]
        for tag in text.tag_names():
            if tag.startswith("color"):
                tags_to_remove.append(tag)
        for tag in tags_to_remove:
            text.tag_remove(tag, "sel.first", "sel.last")


def add_bullets():
    if text.tag_ranges("sel"):
        start_line = int(text.index("sel.first").split('.')[0])
        end_line = int(text.index("sel.last").split('.')[0])
        for line_num in range(start_line, end_line + 1):
            text.insert(f"{line_num}.0", "• ")


def add_numbers():
    if text.tag_ranges("sel"):
        start_line = int(text.index("sel.first").split('.')[0])
        end_line = int(text.index("sel.last").split('.')[0])
        for counter, line_num in enumerate(range(start_line, end_line + 1), 1):
            text.insert(f"{line_num}.0", f"{counter}. ")


def block_quote():
    text.tag_config("blockquote", lmargin1=25, lmargin2=25)
    if text.tag_ranges("sel"):
        text.tag_add("blockquote", "sel.first", "sel.last")


def insert_horizontal_rule():
    text.insert(INSERT, "\n" + ("-" * 50) + "\n")


def apply_code_style():
    text.tag_config("code", font=("Courier", 12), background="#f0f0f0")
    if text.tag_ranges("sel"):
        text.tag_add("code", "sel.first", "sel.last")


def bold():
    text.tag_config("bold", font=(current_font_family, current_font_size, "bold"))
    if text.tag_ranges("sel"):
        if "bold" in text.tag_names("sel.first"):
            text.tag_remove("bold", "sel.first", "sel.last")
        else:
            text.tag_add("bold", "sel.first", "sel.last")


def italic():
    text.tag_config("italic", font=(current_font_family, current_font_size, "italic"))
    if text.tag_ranges("sel"):
        if "italic" in text.tag_names("sel.first"):
            text.tag_remove("italic", "sel.first", "sel.last")
        else:
            text.tag_add("italic", "sel.first", "sel.last")


def underline():
    text.tag_config("underline", underline=True)
    if text.tag_ranges("sel"):
        if "underline" in text.tag_names("sel.first"):
            text.tag_remove("underline", "sel.first", "sel.last")
        else:
            text.tag_add("underline", "sel.first", "sel.last")


def strike():
    text.tag_config("overstrike", overstrike=True)
    if text.tag_ranges("sel"):
        if "overstrike" in text.tag_names("sel.first"):
            text.tag_remove("overstrike", "sel.first", "sel.last")
        else:
            text.tag_add("overstrike", "sel.first", "sel.last")


# ==============================================================================
# VII. UI CONSTRUCTION
#
# Creation of all Tkinter widgets: toolbars, text area, menus, etc.
# ==============================================================================

def create_button_with_icon(parent, icon_name, command_func):
    try:
        full_path = f"icons/{icon_name}"
        photo = Image.open(full_path).resize((18, 18), Resampling.LANCZOS)
        image = ImageTk.PhotoImage(photo)
        button = Button(parent, borderwidth=1, command=command_func, image=image, width=20, height=20)
        button.image = image
        return button
    except:
        return Button(parent, text="?", command=command_func, width=3, height=1)

# --- Toolbars ---
toolbar = Frame(master, pady=2)
undo_button = create_button_with_icon(toolbar, "ic_undo.png", undo)
undo_button.pack(side=LEFT, padx=2, pady=2)
redo_button = create_button_with_icon(toolbar, "ic_redo.png", redo)
redo_button.pack(side=LEFT, padx=2, pady=2)
toolbar.pack(side=TOP, fill=X)

formattingbar = Frame(master, padx=2, pady=2)
buttons = [
    ("ic_text-bold.png", bold), ("ic_text-italic.png", italic),
    ("ic_text-underline.png", underline), ("ic_text-strikethrough.png", strike),
    ("ic_text-color.png", change_font_color), ("ic_text-clear-format.png", clear_formatting)
]
for icon, cmd in buttons:
    btn = create_button_with_icon(formattingbar, icon, cmd)
    btn.pack(side=LEFT, padx=2, pady=2)

ttk.Separator(formattingbar, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=5)

align_buttons = [
    ("ic_text-align-left.png", lambda: text.tag_configure("align_left", justify='left') or text.tag_add("align_left", "1.0", "end")),
    ("ic_text-align-center.png", lambda: text.tag_configure("align_center", justify='center') or text.tag_add("align_center", "1.0", "end")),
    ("ic_text-align-right.png", lambda: text.tag_configure("align_right", justify='right') or text.tag_add("align_right", "1.0", "end"))
]
for icon, cmd in align_buttons:
    btn = create_button_with_icon(formattingbar, icon, cmd)
    btn.pack(side=LEFT, padx=2, pady=2)

ttk.Separator(formattingbar, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=5)

format_buttons = [
    ("ic_list-bulleted.png", add_bullets), ("ic_list-numbered.png", add_numbers),
    ("ic_quotes.png", block_quote), ("ic_inline-code.png", apply_code_style),
    ("ic_horizontal-rule.png", insert_horizontal_rule)
]
for icon, cmd in format_buttons:
    btn = create_button_with_icon(formattingbar, icon, cmd)
    btn.pack(side=LEFT, padx=2, pady=2)

formattingbar.pack(side=TOP, fill=X)

# --- Status Bar and Main Text Area ---
status = Label(master, text="Ready", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

text_frame = Frame(master, borderwidth=1, relief="sunken")
text = Text(text_frame, wrap="word", font=("Arial", 12), background="white",
           borderwidth=0, highlightthickness=0, undo=True)
scrollbar = Scrollbar(text_frame, command=text.yview)
text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
text.pack(side=LEFT, fill=BOTH, expand=True)
text_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

text.focus_set()
text.bind('<KeyRelease>', handle_autocomplete)

# --- Menu Bar ---
menu = Menu(master)
master.config(menu=menu)

file_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new)
file_menu.add_command(label="Open...", command=open_file)
file_menu.add_command(label="Save", command=save)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=close)

edit_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all)

tools_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Tools", menu=tools_menu)
tools_menu.add_command(label="Expand Abbreviations", command=run_abbreviation_expansion)
tools_menu.add_command(label="Analyze Punctuation", command=show_punctuation_analysis)

help_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Simple Text Editor"))


# ==============================================================================
# VIII. APPLICATION EXECUTION
#
# Bind final events and start the Tkinter main event loop.
# ==============================================================================

master.protocol("WM_DELETE_WINDOW", close)
master.mainloop()

import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, font

root = tk.Tk()
root.title("Fixed Text Editor")
root.geometry("900x600")

# ===== Default formatting state for new text =====
default_format = {
    "family": "Arial",
    "size": 14,
    "bold": False,
    "italic": False,
    "underline": False,
    "strike": False,
    "color": "#FFFFFF"
}

# Numbering state
number_counter = 1

# Track where typing starts for fixing last-char bug
last_insert_index = None

# ===== Functions =====
def apply_format_tags(start, end):
    """Apply the current default formatting as tags to the given range."""
    f = font.Font(family=default_format["family"],
                  size=default_format["size"],
                  weight="bold" if default_format["bold"] else "normal",
                  slant="italic" if default_format["italic"] else "roman",
                  underline=1 if default_format["underline"] else 0,
                  overstrike=1 if default_format["strike"] else 0)

    tag_name = (f"font_{default_format['family']}{default_format['size']}"
                f"{default_format['bold']}{default_format['italic']}"
                f"{default_format['underline']}_{default_format['strike']}")

    text.tag_configure(tag_name, font=f)
    text.tag_add(tag_name, start, end)

    color_tag = f"color_{default_format['color']}"
    text.tag_configure(color_tag, foreground=default_format["color"])
    text.tag_add(color_tag, start, end)

def before_typing(event):
    global last_insert_index
    last_insert_index = text.index("insert")

def after_typing(event):
    if not last_insert_index:
        return
    root.after_idle(lambda: apply_format_tags(last_insert_index, "insert"))

def handle_enter(event=None):
    global number_counter
    current_line_num = int(text.index("insert").split(".")[0])
    prev_line_text = text.get(f"{current_line_num - 1}.0", f"{current_line_num - 1}.end")

    # Continue bullet
    if prev_line_text.strip().startswith("•"):
        text.insert("insert", "\n• ")
        return "break"

    # Continue numbering
    first_word = prev_line_text.strip().split(" ")[0]
    if first_word.replace(".", "").isdigit():
        try:
            num = int(first_word.replace(".", "")) + 1
        except ValueError:
            num = number_counter
        text.insert("insert", f"\n{num}. ")
        number_counter = num
        return "break"

    return None

def toggle_format(attr):
    try:
        start, end = text.index(tk.SEL_FIRST), text.index(tk.SEL_LAST)
        default_format[attr] = not default_format[attr]
        apply_format_tags(start, end)
    except tk.TclError:
        default_format[attr] = not default_format[attr]

def toggle_bold(): toggle_format("bold")
def toggle_italic(): toggle_format("italic")
def toggle_underline(): toggle_format("underline")
def toggle_strike(): toggle_format("strike")

def change_font_family(event=None):
    try:
        start, end = text.index(tk.SEL_FIRST), text.index(tk.SEL_LAST)
        default_format["family"] = font_var.get()
        apply_format_tags(start, end)
    except tk.TclError:
        default_format["family"] = font_var.get()

def change_font_size(event=None):
    try:
        start, end = text.index(tk.SEL_FIRST), text.index(tk.SEL_LAST)
        default_format["size"] = size_var.get()
        apply_format_tags(start, end)
    except tk.TclError:
        default_format["size"] = size_var.get()

def adjust_font_size(delta):
    size_var.set(max(6, size_var.get() + delta))
    change_font_size()

def change_color():
    color = colorchooser.askcolor(title="Pick a color")[1]
    if color:
        try:
            start, end = text.index(tk.SEL_FIRST), text.index(tk.SEL_LAST)
            default_format["color"] = color
            apply_format_tags(start, end)
        except tk.TclError:
            default_format["color"] = color

def toggle_bullet():
    line_start = f"{text.index(tk.INSERT).split('.')[0]}.0"
    line_text = text.get(line_start, f"{line_start} lineend")
    if line_text.strip().startswith("•"):
        text.delete(line_start, f"{line_start}+2c")
    else:
        text.insert(line_start, "• ")

def toggle_numbering():
    global number_counter
    line_start = f"{text.index(tk.INSERT).split('.')[0]}.0"
    line_text = text.get(line_start, f"{line_start} lineend")
    if line_text.strip().split(" ")[0].replace(".", "").isdigit():
        text.delete(line_start, f"{line_start}+4c")
    else:
        text.insert(line_start, f"{number_counter}. ")
        number_counter += 1

def undo():
    try:
        text.edit_undo()
    except tk.TclError:
        messagebox.showinfo("Undo", "Nothing left to undo.")

def redo():
    try:
        text.edit_redo()
    except tk.TclError:
        messagebox.showinfo("Redo", "Nothing left to redo.")

# ===== Toolbar =====
toolbar = tk.Frame(root, bg="#333333")
toolbar.pack(side=tk.TOP, fill=tk.X)

# Font family dropdown
fonts_list = sorted(list(font.families()))
font_var = tk.StringVar(value=default_format["family"])
font_dropdown = tk.OptionMenu(toolbar, font_var, *fonts_list, change_font_family)
font_dropdown.pack(side=tk.LEFT, padx=2, pady=2)

# Font size dropdown
size_var = tk.IntVar(value=default_format["size"])
sizes = list(range(8, 73, 2))
size_dropdown = tk.OptionMenu(toolbar, size_var, *sizes, change_font_size)
size_dropdown.pack(side=tk.LEFT, padx=2, pady=2)

# Increase/Decrease size
tk.Button(toolbar, text="A+", command=lambda: adjust_font_size(1)).pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="A-", command=lambda: adjust_font_size(-1)).pack(side=tk.LEFT, padx=2)

# Formatting buttons
tk.Button(toolbar, text="B", command=toggle_bold).pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="I", command=toggle_italic).pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="U", command=toggle_underline).pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="S", command=toggle_strike).pack(side=tk.LEFT, padx=2)

# Color button
tk.Button(toolbar, text="Color", command=change_color).pack(side=tk.LEFT, padx=2)

# Bullets & numbering
tk.Button(toolbar, text="•", command=toggle_bullet).pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="1.", command=toggle_numbering).pack(side=tk.LEFT, padx=2)

# Undo / Redo
tk.Button(toolbar, text="Undo", command=undo).pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="Redo", command=redo).pack(side=tk.LEFT, padx=2)

# ===== Text widget =====
text = tk.Text(root, wrap="word", undo=True,
               bg="#1E1E1E", fg=default_format["color"],
               insertbackground="white")
text.pack(fill=tk.BOTH, expand=True)

# Bindings
text.bind("<KeyPress>", before_typing)
text.bind("<KeyRelease>", after_typing)
text.bind("<Return>", handle_enter)

root.mainloop()
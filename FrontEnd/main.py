import tkinter as tk
from tkinter import ttk

# --- Constants remain the same ---
BG_COLOR = "#F7F7F7"
TOOLBAR_COLOR = "#EEEEEE"
FONT_FAMILY = "Segoe UI"
FONT_SIZE = 10

# --- Helper functions for creating individual buttons ---

def create_toolbar_button(parent, text, command):
    """Creates a styled TEXT button and places it in the parent."""
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=(FONT_FAMILY, FONT_SIZE, "bold"),
        bg=TOOLBAR_COLOR,
        relief=tk.FLAT,
        bd=0,
        width=3,
        activebackground="#D0D0D0"
    )
    button.pack(side=tk.LEFT, padx=2, pady=2)
    return button

def create_toolbar_radiobutton(parent, text, variable, value, command):
    """Creates a styled TEXT radiobutton and places it in the parent."""
    radio_btn = tk.Radiobutton(
        parent,
        text=text,
        variable=variable,
        value=value,
        command=command,
        font=(FONT_FAMILY, FONT_SIZE, "bold"),
        indicatoron=0,
        bg=TOOLBAR_COLOR,
        selectcolor="#C0C0C0",
        relief=tk.FLAT,
        bd=0,
        width=3,
        activebackground="#D0D0D0"
    )
    radio_btn.pack(side=tk.LEFT, padx=2, pady=2)
    return radio_btn

# --- Main functions to build the UI ---

def create_toolbar(parent, state, callbacks):
    """Creates the entire top toolbar."""
    toolbar_frame = tk.Frame(parent, bg=TOOLBAR_COLOR, bd=1, relief=tk.SOLID)
    toolbar_frame.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(2, 0))

    # Style Dropdown
    style_options = ["Paragraph", "Heading 1", "Heading 2", "Heading 3"]
    state["style_var"] = tk.StringVar(value=style_options[0])
    style_dropdown = ttk.Combobox(
        toolbar_frame,
        textvariable=state["style_var"],
        values=style_options,
        width=15,
        font=(FONT_FAMILY, FONT_SIZE),
        state="readonly"
    )
    style_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

    # Buttons
    create_toolbar_button(toolbar_frame, "B", callbacks["on_bold"])
    create_toolbar_button(toolbar_frame, "I", callbacks["on_italic"])
    create_toolbar_button(toolbar_frame, "U", callbacks["on_underline"])

    # Separator
    ttk.Separator(toolbar_frame, orient='vertical').pack(side=tk.LEFT, padx=5, pady=5, fill='y')

    # Alignment Radiobuttons
    create_toolbar_radiobutton(toolbar_frame, "L", state["align_var"], "left", callbacks["on_align"])
    create_toolbar_radiobutton(toolbar_frame, "C", state["align_var"], "center", callbacks["on_align"])
    create_toolbar_radiobutton(toolbar_frame, "R", state["align_var"], "right", callbacks["on_align"])

    return toolbar_frame

def create_text_area(parent):
    """Creates the main text editing area."""
    text_area = tk.Text(
        parent,
        wrap=tk.WORD,
        font=(FONT_FAMILY, 12),
        bd=0,
        relief=tk.FLAT,
        padx=10,
        pady=10
    )
    text_area.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    text_area.insert(tk.END, "Type your text here...")
    return text_area

# --- Main Application Logic ---

def main():
    """Initializes the application and runs the main loop."""
    root = tk.Tk()
    root.title("Functional Text Editor")
    root.geometry("700x500")
    root.configure(bg=BG_COLOR)

    # This dictionary holds the application's state, replacing `self`.
    app_state = {
        "align_var": tk.StringVar(value="left"),
        "style_var": None,
        "text_area": None
    }

    # Define callback functions here so they have access to `app_state`.
    # This is a 'closure'.
    def on_bold_click():
        print("Bold button clicked!")
        # Example: to access the text area, you would use app_state['text_area']

    def on_italic_click():
        print("Italic button clicked!")

    def on_underline_click():
        print("Underline button clicked!")

    def on_align_click():
        alignment = app_state["align_var"].get()
        print(f"Alignment set to: {alignment}")

    # A dictionary to hold the callback functions for easy passing.
    callbacks = {
        "on_bold": on_bold_click,
        "on_italic": on_italic_click,
        "on_underline": on_underline_click,
        "on_align": on_align_click
    }

    # Create the UI components
    create_toolbar(root, app_state, callbacks)
    # Store the created text_area in our state dictionary so callbacks can use it
    app_state["text_area"] = create_text_area(root)

    root.mainloop()

# --- Entry point of the script ---
if __name__ == "__main__":
    main()

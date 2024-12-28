from fontTools.ttLib import TTFont
import tkinter as tk
from tkinter import filedialog

def get_chars(font_path):
    font = TTFont(font_path)
    chars = []
    cmap = font['cmap'].getBestCmap()
    for code, glyph in cmap.items():
        chars.append((chr(code), f"U+{code:04X}"))
    return chars

def save(chars, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for char, code in chars:
            file.write(f"{char} [{code}]\n")

def main():
    root = tk.Tk()
    root.withdraw()
    font_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Font File", "*.otf *.ttf *.woff *.woff2")]
    )

    if not font_path:
        print("Choose a file")
        return

    chars = get_chars(font_path)

    output_path = filedialog.asksaveasfilename(
        title="Save sheet to...",
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt")]
    )
    
    if not output_path:
        print("Choose a directory")
        return

    save(chars, output_path)

    print(f"Sheet have been saved in {output_path}")

if __name__ == "__main__":
    main()

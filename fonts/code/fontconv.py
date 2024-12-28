import tkinter as tk
from tkinter import filedialog
import os
from fontTools.ttLib import TTFont

def main():
    root = tk.Tk()
    root.withdraw()
    font_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Font File", "*.otf *.ttf")]
    )

    if not font_path:
        print("Choose a file")
        return

    output_path = os.path.splitext(font_path)[0] + ".woff2"
    font = TTFont(font_path)
    font.flavor = 'woff2'
    font.save(output_path)
    print(f"Converted in {output_path}")

if __name__ == "__main__":
    main()

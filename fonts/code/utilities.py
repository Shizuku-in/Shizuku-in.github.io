import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
from fontTools.ttLib import TTFont
import subprocess
import threading

def compress_webp(file_path, quality):
    """Compress an image file to WebP format."""
    try:
        img = Image.open(file_path)
        webp_path = os.path.splitext(file_path)[0] + ".webp"
        img.save(webp_path, "webp", quality=quality)
        return webp_path
    except Exception as e:
        return f"Error: {e}"

def create_font_subset(font_path, txt_path, save_woff2, save_sheet):
    """Create a font subset using pyftsubset."""
    try:
        # Read characters from the txt file
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Generate the subset font command
        subset_output = os.path.splitext(font_path)[0] + "_subset"
        if save_woff2:
            subset_output += ".woff2"
        else:
            subset_output += ".ttf"

        cmd = [
            "pyftsubset",
            font_path,
            f"--text={text}",
            f"--output-file={subset_output}",
        ]

        if save_woff2:
            cmd.append("--flavor=woff2")

        subprocess.run(cmd, check=True)

        # Generate character mapping sheet if required
        if save_sheet:
            font = TTFont(font_path)
            subset_font = TTFont(subset_output)
            cmap = subset_font["cmap"].tables[0].cmap
            sorted_mapping = sorted(cmap.items(), key=lambda x: x[0])

            sheet_output = subset_output + "_mapping.txt"
            with open(sheet_output, "w", encoding="utf-8") as sheet:
                for code, char in sorted_mapping:
                    sheet.write(f"{chr(code)} [U+{code:04X}]\n")

        return subset_output
    except Exception as e:
        return f"Error: {e}"

def process_webp(file_paths, quality_var, progress_var, progress_bar):
    """Process WebP compression in a separate thread."""
    total = len(file_paths)
    progress_var.set(0)
    for i, file_path in enumerate(file_paths, 1):
        compress_webp(file_path, quality_var.get())
        progress_var.set(i / total * 100)
        progress_bar.update()

def process_font_subset(font_path, txt_path, woff2_var, sheet_var, progress_bar):
    """Process Font Subset creation in a separate thread."""
    create_font_subset(font_path, txt_path, woff2_var.get(), sheet_var.get())
    progress_bar["value"] = 100
    progress_bar.update()
    messagebox.showinfo("Fontsubset Maker", "Complete!")

def setup_gui():
    root = TkinterDnD.Tk()
    root.title("Utilities")

    # Main layout
    left_frame = tk.Frame(root, width=200)
    left_frame.pack(side="left", fill="y")
    right_frame = tk.Frame(root)
    right_frame.pack(side="right", fill="both", expand=True)

    # Create frames for each tool
    webp_frame = tk.Frame(right_frame)
    fontsubset_frame = tk.Frame(right_frame)

    # Function to show WebP Compressor UI
    def select_webp():
        webp_frame.pack(fill="both", expand=True)
        fontsubset_frame.pack_forget()

    # Function to show Fontsubset Maker UI
    def select_fontsubset():
        fontsubset_frame.pack(fill="both", expand=True)
        webp_frame.pack_forget()

    # Left column buttons
    tk.Button(left_frame, text="WebP Compressor", command=select_webp).pack(fill="x")
    tk.Button(left_frame, text="Fontsubset Maker", command=select_fontsubset).pack(fill="x")

    # WebP Compressor Frame
    tk.Label(webp_frame, text="Drop images or folders here~").pack()

    quality_label = tk.Label(webp_frame, text="Quality:")
    quality_label.pack()

    quality_var = tk.IntVar(value=80)
    quality_slider = tk.Scale(webp_frame, from_=0, to=100, orient="horizontal", variable=quality_var)
    quality_slider.pack()

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(webp_frame, variable=progress_var, maximum=100)
    progress_bar.pack(fill="x")

    def handle_webp_drop(event):
        print(f"WebP drop event data: {event.data}")  # 调试输出
        paths = root.splitlist(event.data)
        threading.Thread(target=process_webp, args=(paths, quality_var, progress_var, progress_bar)).start()

    try:
        webp_frame.drop_target_register(DND_FILES)
        webp_frame.dnd_bind("<<Drop>>", handle_webp_drop)
    except Exception as e:
        print(f"Error binding WebP drop: {e}")

    # Fontsubset Maker Frame
    tk.Label(fontsubset_frame, text="Drop a font file and a txt file here~").pack()

    woff2_var = tk.BooleanVar(value=False)
    tk.Checkbutton(fontsubset_frame, text="WOFF2 Compress", variable=woff2_var).pack()

    sheet_var = tk.BooleanVar(value=False)
    tk.Checkbutton(fontsubset_frame, text="Save Mappingsheet", variable=sheet_var).pack()

    progress_bar_font = ttk.Progressbar(fontsubset_frame, maximum=100)
    progress_bar_font.pack(fill="x")

    def handle_font_drop(event):
        print(f"Font drop event data: {event.data}")  # 调试输出
        paths = root.splitlist(event.data)
        font_path, txt_path = None, None
        for path in paths:
            if path.endswith(".ttf") or path.endswith(".otf"):
                font_path = path
            elif path.endswith(".txt"):
                txt_path = path
        if font_path and txt_path:
            threading.Thread(target=process_font_subset, args=(font_path, txt_path, woff2_var, sheet_var, progress_bar_font)).start()
        else:
            messagebox.showerror("Error", "Please drop both a font file and a txt file.")

    try:
        fontsubset_frame.drop_target_register(DND_FILES)
        fontsubset_frame.dnd_bind("<<Drop>>", handle_font_drop)
    except Exception as e:
        print(f"Error binding Font drop: {e}")

    # Show initial frame
    select_webp()

    root.mainloop()

if __name__ == "__main__":
    setup_gui()

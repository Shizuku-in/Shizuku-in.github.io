import os
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
from fontTools.ttLib import TTFont
import subprocess
import threading
from tkinter import messagebox



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
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()

        subset_output = os.path.splitext(font_path)[0] + "_subset"
        subset_output += ".woff2" if save_woff2 else ".ttf"

        cmd = ["pyftsubset", font_path, f"--text={text}", f"--output-file={subset_output}"]
        if save_woff2:
            cmd.append("--flavor=woff2")

        subprocess.run(cmd, check=True)

        if save_sheet:
            font = TTFont(font_path)
            subset_font = TTFont(subset_output)
            cmap = subset_font["cmap"].tables[0].cmap
            sorted_mapping = sorted(cmap.items(), key=lambda x: x[0])

            sheet_output = subset_output + "_mapping.txt"
            with open(sheet_output, "w", encoding="utf-8") as sheet:
                for code, char in sorted_mapping:
                    sheet.write(f"{char} [U+{code:04X}]\n")

        return subset_output
    except Exception as e:
        return f"Error: {e}"

def process_webp(file_paths, quality_var, progress_var, progress_bar):
    total = len(file_paths)
    progress_var.set(0)
    for i, file_path in enumerate(file_paths, 1):
        compress_webp(file_path, quality_var.get())
        progress_var.set(i / total * 100)
        progress_bar.update()
    messagebox.showinfo("WebP Compressor", "Compression complete!")

def process_font_subset(font_path, txt_path, woff2_var, sheet_var, progress_bar):
    create_font_subset(font_path, txt_path, woff2_var.get(), sheet_var.get())
    progress_bar.set(100)
    messagebox.showinfo("Fontsubset Maker", "Font subset creation complete!")

def setup_gui():
    ctk.set_appearance_mode("System")  # 主题：系统/暗色/亮色
    ctk.set_default_color_theme("blue")  # 默认颜色主题

    root = ctk.CTk()
    root.title("WebP Compressor & Fontsubset Maker")
    root.geometry("800x500")

    left_frame = ctk.CTkFrame(root, width=200, corner_radius=10)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)
    right_frame = ctk.CTkFrame(root, corner_radius=10)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    webp_frame = ctk.CTkFrame(right_frame, corner_radius=10)
    fontsubset_frame = ctk.CTkFrame(right_frame, corner_radius=10)

    def select_webp():
        webp_frame.pack(fill="both", expand=True)
        fontsubset_frame.pack_forget()

    def select_fontsubset():
        fontsubset_frame.pack(fill="both", expand=True)
        webp_frame.pack_forget()

    ctk.CTkButton(left_frame, text="WebP Compressor", command=select_webp).pack(fill="x", pady=5)
    ctk.CTkButton(left_frame, text="Fontsubset Maker", command=select_fontsubset).pack(fill="x", pady=5)

    # WebP Compressor
    ctk.CTkLabel(webp_frame, text="Drag and drop images or folders:").pack(pady=10)
    quality_var = ctk.IntVar(value=80)
    ctk.CTkLabel(webp_frame, text="Quality:").pack()
    ctk.CTkSlider(webp_frame, from_=0, to=100, variable=quality_var).pack(fill="x", pady=10)

    progress_var = ctk.IntVar()
    progress_bar = ctk.CTkProgressBar(webp_frame, variable=progress_var)
    progress_bar.pack(fill="x", pady=10)

    def handle_webp_drop(event):
        paths = root.splitlist(event.data)
        threading.Thread(target=process_webp, args=(paths, quality_var, progress_var, progress_bar)).start()

    webp_frame.drop_target_register(DND_FILES)
    webp_frame.dnd_bind("<<Drop>>", handle_webp_drop)

    # Fontsubset Maker
    ctk.CTkLabel(fontsubset_frame, text="Drag and drop a font file and a txt file:").pack(pady=10)

    woff2_var = ctk.BooleanVar(value=False)
    ctk.CTkCheckBox(fontsubset_frame, text="WOFF2 Compress", variable=woff2_var).pack()

    sheet_var = ctk.BooleanVar(value=False)
    ctk.CTkCheckBox(fontsubset_frame, text="Save Sheet", variable=sheet_var).pack()

    progress_bar_font = ctk.CTkProgressBar(fontsubset_frame)
    progress_bar_font.pack(fill="x", pady=10)

    def handle_font_drop(event):
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

    fontsubset_frame.drop_target_register(DND_FILES)
    fontsubset_frame.dnd_bind("<<Drop>>", handle_font_drop)

    select_webp()
    root.mainloop()

if __name__ == "__main__":
    setup_gui()

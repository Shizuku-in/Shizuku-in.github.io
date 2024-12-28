import requests
from bs4 import BeautifulSoup
import re
import subprocess
import os
from fontTools.ttLib import TTFont

def fetch_text(url): # 获取涵盖字符
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f"Can't access {url}: {e}")
        return ""

def get_chars(text):
    return sorted(set(re.findall(r'[^\s]', text)), key=ord)

def make_subset(font, chars, out_dir): # 制作字体子集
    try:
        font_name = os.path.basename(font)
        name_no_ext = os.path.splitext(font_name)[0]
        subset_path = os.path.join(out_dir, f"{name_no_ext}_subset.woff2")
        subprocess.run([
            "pyftsubset",
            font,
            f"--text={''.join(chars)}",
            "--flavor=woff2",
            f"--output-file={subset_path}"
        ], check=True)
        print(f"Subset saved to: {subset_path}")
        return subset_path
    except Exception as e:
        print(f"Error when generating subset: {e}")
        return None

def write_sheet(font, out_dir): # 打印映射表
    try:
        tt = TTFont(font)
        cmap = tt['cmap'].getBestCmap()
        sheet_path = os.path.join(out_dir, "table.txt")
        total_chars = len(cmap)
        with open(sheet_path, "w", encoding="utf-8") as f:
            f.write(f"Total: {total_chars}\n------\n")
            for code, char in cmap.items():
                f.write(f"{chr(code)} [U+{code:04X}]\n")
        print(f"Mapping table saved to: {sheet_path}")
    except Exception as e:
        print(f"Error when generating mapping table: {e}")

def main():
    urls = input("URLs: ").split()
    chars = []
    for url in urls:
        print(f"Process: {url}")
        text = fetch_text(url)
        if text:
            chars.extend(get_chars(text))
    chars = sorted(set(chars), key=ord)
    
    font = input("Font: ").strip()
    if not os.path.isfile(font):
        print("The file doesn't exist")
        return
    
    out_dir = os.path.dirname(font)
    subset_font = make_subset(font, chars, out_dir)
    if subset_font:
        write_sheet(subset_font, out_dir)

if __name__ == "__main__":
    main()

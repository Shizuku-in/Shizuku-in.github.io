import os
import webp
from PIL import Image

def main(dir):
    if not os.path.isdir(dir):
        print("The dir doesn't exist")
        return

    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                im = Image.open(file_path)
                webp_path = os.path.splitext(file_path)[0] + '.webp'
                webp.save_image(im, webp_path, quality=90)  # quality
                print(f"{filename} -> {webp_path}")
            except Exception as e:
                print(f"Error happened when processing {filename}: {e}")

if __name__ == "__main__":
    dir = input("directory: ")
    main(dir)
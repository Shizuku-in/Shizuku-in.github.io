import os
import webp
from PIL import Image

def main(directory):
    if not os.path.isdir(directory):
        print("The directory doesn't exist")
        return

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                im = Image.open(file_path)
                webp_path = os.path.splitext(file_path)[0] + '.webp'
                webp.save_image(im, webp_path, quality=70) # quality
                print(f"{filename} -> {webp_path}")
            except Exception as e:
                print(f"Error happened when processing {filename}: {e}")

if __name__ == "__main__":
    directory = input("Directory: ")
    main()
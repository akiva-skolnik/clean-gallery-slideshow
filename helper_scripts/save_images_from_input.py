import os
import traceback

destination = input("Enter the destination directory: ")
paths_file = os.path.join(destination, "original_paths.txt")
existing_paths = os.path.join(destination, "existing_paths.txt")

# This script takes a list of image paths and link them to a destination directory while logging the paths to a file.
with (open(paths_file, "a", encoding="utf-8") as mapped_paths_file,
      open(existing_paths, "a", encoding="utf-8") as existing_paths_file):
    while True:
        try:
            images = input("Enter the path to the images: ")
            if images == "exit":
                break
            images = [image.strip('"') for image in (images.split('" "') if '"' in images else images.split())]
            for image in images:
                if not os.path.exists(image):
                    print(f"File {image} does not exist")
                    continue

                dest_path = os.path.join(destination, os.path.basename(image))
                # If the destination path already exists, append 1 to the name as many times as necessary.
                while os.path.exists(dest_path):
                    existing_paths_file.write(f"{image}\n")
                    name, extension = dest_path.split(".")
                    new_name = name + "1." + extension
                    dest_path = os.path.join(destination, new_name)

                os.link(image, dest_path)
                mapped_paths_file.write(f"{image}|{dest_path}\n")
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            # break

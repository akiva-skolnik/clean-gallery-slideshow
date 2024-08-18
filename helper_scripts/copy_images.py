import os

from PIL import Image


def read_excluded_paths(excluded_file_path: str) -> set:
    """
    The excluded file contains lines in the format: "/path/to/image.jpg|/path/to/shortcut.jpg"
    We only need the original path, so we split the line and take the first part
    We also remove the drive letter and the first two backslashes, because it may vary.
    """
    with open(excluded_file_path, 'r', encoding="utf-8") as excluded_file:
        return {line.strip().split('|')[0][2:].strip("/\\") for line in excluded_file}


def fix_image_orientation(image: Image) -> Image:
    """Check and fix image orientation using EXIF data"""
    if hasattr(image, "_getexif"):
        exif = image.getexif()
        if exif is not None:
            orientation = exif.get(274)  # 274 is the orientation tag
            # orientation 1 is normal, 2 is mirrored horizontally, 3 is rotated 180, 4 is mirrored vertically,
            # 5 is mirrored horizontally then rotated 90 CCW, 6 is rotated 90 CW,
            # 7 is mirrored horizontally then rotated 90 CW, and 8 is rotated 90 CCW
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    return image


def copy_images(source_folder: str,
                destination_folder: str,
                excluded_paths: set,
                mapped_paths_file_name: str = "mapped_paths.txt",
                desired_image_size: tuple = (1366, 768),
                max_images_per_subfolder: int = 2 ** 15  # Bash RANDOM range is 0-32767
                ):
    """ copy images from source_folder to destination_folder, resizing them to desired_image_size
        - the destination_folder will be divided into subfolders,
            each contain images named 0...max_images_per_subfolder (to avoid duplicate names)
        - the excluded_paths is a set of paths that should not be copied
    """

    print(f"Copying images from {source_folder} to {destination_folder}")
    # Create the first subfolder
    current_subfolder = 0
    current_subfolder_path = os.path.join(destination_folder, str(current_subfolder))
    os.makedirs(current_subfolder_path, exist_ok=True)

    # Skip the first skip_images images
    skip_images = 0
    skipped = False
    image_count = 0
    # This file can be very large, so I split it into multiple files (one per subfolder)
    mapped_paths_file_path = os.path.join(current_subfolder_path, mapped_paths_file_name)
    mapped_paths_file = open(mapped_paths_file_path, 'a', encoding="utf-8")
    # Traverse the source folder and copy images to the destination folder
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Remove double slashes and backslashes from the source folder path, and remove the drive letter
                source_path = os.path.join(root, file)
                partial_source_path = source_path.replace("//", "/").replace("\\\\", "\\")[2:].strip("/\\")

                # Check if the image path is not in the excluded set
                if partial_source_path not in excluded_paths:  # excluded_paths is a set, so this is O(1)
                    if not skipped and image_count < skip_images:
                        image_count += 1
                        continue
                    else:
                        skipped = True

                    # Create a new filename (0...n)
                    new_filename = str(image_count) + ".jpg"

                    # Create the destination path in the current subfolder
                    destination_path = os.path.join(current_subfolder_path, new_filename)
                    try:
                        image = Image.open(source_path)
                    except Exception as e:
                        print(f"Failed to open {source_path}: " + str(e))
                        continue
                    # Resize while preserving aspect ratio
                    try:
                        image.thumbnail(desired_image_size, Image.LANCZOS)
                    except Exception as e:
                        print(f"Failed to resize {source_path}: " + str(e))
                        continue
                    image = fix_image_orientation(image)
                    # Save the image without EXIF data
                    image.save(destination_path, "JPEG", exif=b'')
                    mapped_paths_file.write(f"{source_path}|{destination_path}\n")

                    # Increment image count
                    image_count += 1

                    # Check if the current subfolder is full
                    if image_count == max_images_per_subfolder:
                        # Move to the next subfolder
                        current_subfolder += 1
                        current_subfolder_path = os.path.join(destination_folder, str(current_subfolder))
                        os.makedirs(current_subfolder_path, exist_ok=True)
                        image_count = 0
                        mapped_paths_file.close()
                        mapped_paths_file_path = os.path.join(current_subfolder_path, mapped_paths_file_name)
                        mapped_paths_file = open(mapped_paths_file_path, 'a', encoding="utf-8")
    mapped_paths_file.close()


if __name__ == "__main__":
    source_folder = input("Enter the source folder: ")
    destination_folder = os.path.split(source_folder)[0]
    excluded_file_path = os.path.join(destination_folder, "original_paths.txt")
    copy_images(source_folder=source_folder,
                destination_folder=destination_folder,
                excluded_paths=read_excluded_paths(excluded_file_path=excluded_file_path))

import datetime
import os

from PIL import Image
from PIL.ExifTags import TAGS


def get_exif(filename: str) -> dict:
    image = Image.open(filename)
    image.verify()
    try:
        return image._getexif()  # _ gives more info
    except Exception as e:
        print(f"Failed to get exif data for {filename}: {e}")
        return {}


def get_exif_data(filename: str) -> dict:
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = get_exif(filename)
    return {
        TAGS[k]: v
        for k, v in exif_data.items()
        if k in TAGS
    }


def get_date_taken(filename: str) -> datetime.datetime or None:
    """Get the date the picture was taken"""
    date_time_original = get_exif_data(filename).get('DateTimeOriginal')
    if date_time_original is None:
        return None
    return datetime.datetime.strptime(date_time_original, "%Y:%m:%d %H:%M:%S")


def main():
    # sort images to a new folder using link (to save space) according to the date they were taken
    source_folder = input("Enter the source folder: ")
    destination_folder = os.path.join(source_folder, "sorted_images")
    os.makedirs(destination_folder, exist_ok=True)

    created_time_mapping = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                source_path = os.path.join(root, file)
                date_taken = get_date_taken(source_path) or datetime.datetime.now()
                created_time_mapping.append((source_path, date_taken))
        break  # only the first level

    created_time_mapping.sort(key=lambda x: x[1])
    with open(os.path.join(destination_folder, "original_paths.txt"), 'w', encoding="utf-8") as mapped_paths_file:
        for index, (source_path, date_taken) in enumerate(created_time_mapping):
            # 4 digits for the index
            new_filename = f"{index:04d}.jpg"
            destination_path = os.path.join(destination_folder, new_filename)
            os.link(source_path, destination_path)
            print(f"{source_path} -> {destination_path}")
            mapped_paths_file.write(f"{source_path}|{destination_path}\n")


if __name__ == "__main__":
    main()

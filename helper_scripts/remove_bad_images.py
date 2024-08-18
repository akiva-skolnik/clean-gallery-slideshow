import os


def delete_original_images(original_shortcut_paths: list) -> None:
    for original_path, shortcut_path in original_shortcut_paths:
        if not os.path.exists(shortcut_path):
            # If the shortcut doesn't exist, delete the original image
            os.remove(original_path)
            print(f"Deleted original image: {original_path}")


# Read the text file with original and shortcut paths
output_dir = input("Enter the output directory: ")
original_paths_file = os.path.join(output_dir, 'original_paths.txt')

with open(original_paths_file, 'r', encoding="utf-8") as paths_file:
    # pairs of original_path, shortcut_path
    original_shortcut_paths = [line.strip().split('|') for line in paths_file]

# Call the function to delete original images
delete_original_images(original_shortcut_paths)

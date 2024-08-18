import argparse
import os
import random


def generate_random_file_lists(source_dir: str, target_dir: str, num_files: int) -> None:
    """Write random file paths from source_dir to txt files, 1000 files per txt file."""
    # Create target_dir if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Get all file paths from source_dir
    file_paths = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".jpg"):
                # assume source_dir contains /images
                file_paths.append("/home/pi/images/" + root.split("/images")[-1].replace("\\", "") + "/" + file)

    # Randomly shuffle file paths
    random.shuffle(file_paths)

    # Write file paths to txt files
    num_txt_files = len(file_paths) // num_files + 1
    for i in range(num_txt_files):
        with open(os.path.join(target_dir, str(i) + '.txt'), 'w') as f:
            for file_path in file_paths[i * num_files: (i + 1) * num_files]:
                f.write(file_path + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_dir', type=str)
    parser.add_argument('--target_dir', type=str)
    parser.add_argument('--num_files', type=int, default=1000)
    args = parser.parse_args()
    generate_random_file_lists(args.source_dir, args.target_dir, args.num_files)

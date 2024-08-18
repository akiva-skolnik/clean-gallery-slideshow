import os

import cv2
import numpy as np

# Define input and output directories
input_dir = input("Enter the input directory: ")
output_dir = 'temp'
os.makedirs(output_dir, exist_ok=True)

# Set the blurriness threshold (adjust as needed)
threshold = 200


# Function to calculate blurriness
def calculate_blur_1(image: np.ndarray) -> float:
    return cv2.Laplacian(image, cv2.CV_64F).var()


def calculate_blur_2(image_path: str) -> float:
    gray = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    gradient_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    gradient_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    magnitude = cv2.magnitude(gradient_x, gradient_y)
    return magnitude.var()


def calculate_blur_3(image: np.ndarray) -> float:
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    gradient_x = cv2.filter2D(image, -1, kernel_x)
    gradient_y = cv2.filter2D(image, -1, kernel_y)
    gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
    return np.mean(gradient_magnitude) * 100


def is_overexposed(image_path: str) -> bool:
    img = cv2.imread(image_path)
    return img.mean() > 200


def how_bad_images(image: np.ndarray) -> float:
    blur = cv2.blur(image, (10, 10))
    return np.sum(blur) / (image.shape[0] * image.shape[1])


def detect_bad_images1(image: np.ndarray, threshold: float = 127) -> bool:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]
    return np.mean(binary)


def is_bad_images(image: np.ndarray) -> bool:
    mask = np.zeros_like(image, dtype=np.uint8)
    mask[100:200, 100:200] = 255
    inpainted_image = cv2.inpaint(image, mask, 1, cv2.INPAINT_TELEA)
    return not np.array_equal(image, inpainted_image)


def main():
    index = 1
    original_paths_file = os.path.join(output_dir, 'original_paths.txt')
    # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    with open(original_paths_file, 'w', encoding='utf-8') as paths_file:
        for root, dirs, files in os.walk(input_dir):
            for filename in files:
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):  # Add more image extensions if needed
                    image_path = os.path.join(root, filename)
                    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    # faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                    # m = image.mean()
                    m = is_bad_images(image)
                    if m:
                        # Generate a unique filename for the shortcut
                        shortcut_filename = f'{int(m * 100):07d}_{index}_{filename}'
                        shortcut_path = os.path.join(output_dir, shortcut_filename)

                        # Create a shortcut to the original image
                        os.link(image_path, shortcut_path)
                        # Write the original path, shortcut path, and normalized filename to the text file
                        paths_file.write(f'{image_path}|{shortcut_path}\n')

                        index += 1

    print("Images copied as shortcuts and paths recorded.")


if __name__ == '__main__':
    main()

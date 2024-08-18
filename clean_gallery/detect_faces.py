import os

import cv2  # pip install opencv-python
import numpy as np

# Define input and output directories
input_dir = input("Enter the input directory: ")
output_dir = os.path.join(input_dir, 'no_faces')
os.makedirs(output_dir, exist_ok=True)
original_paths_file = os.path.join(output_dir, 'original_paths.txt')

# Download here: https://github.com/gopinath-balu/computer_vision/blob/master/CAFFE_DNN/res10_300x300_ssd_iter_140000.caffemodel
net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")
index = 1


def get_image_paths_from_file() -> (str, str):
    global index
    skip_up_to = ""  # you can set this to the last processed image to skip up to that point
    with open(os.path.join(input_dir, 'original_paths.txt'), 'r', encoding="utf-8") as paths_file1:
        for line in paths_file1:
            original_path, image_path = line.strip().split('|')
            if skip_up_to:
                if str(original_path) == skip_up_to:
                    skip_up_to = ""
                    index += 1
                continue
            yield original_path, image_path


def get_image_paths_from_folder() -> (str, str):
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Add more image extensions if needed
                continue
            image_path = os.path.join(root, filename)
            yield image_path, image_path


def get_max_confidence(image: np.ndarray) -> float:
    (height, width) = (300, 300)  # other options: (416, 416), (299, 299), image.shape[:2]
    mean = (104, 177, 123)  # or (104, 117, 123)
    blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(height, width), mean=mean)  # , swapRB=True, crop=False)
    net.setInput(blob)
    max_confidence = np.max(net.forward()[0, 0, :, 2])
    return max_confidence


# def get_max_confidence(image: np.ndarray, threshold: float = 0.3) -> float:
#     from retinaface import RetinaFace
#     face_detection_result = RetinaFace.detect_faces(image, threshold=threshold, allow_upscaling=False)
#     max_confidence = max(face["score"] for face in face_detection_result.values()) \
#         if isinstance(face_detection_result, dict) else 0
#     return max_confidence

# Another way to detect faces using dlib:
# import dlib
# detector = dlib.get_frontal_face_detector()
# faces = detector(gray_image)


def main():
    global index
    with open(original_paths_file, 'a', encoding='utf-8') as paths_file:
        for original_path, image_path in get_image_paths_from_file():
            image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            try:
                resized_image = cv2.resize(image, (300, 300))
            except Exception as e:
                print("skipped", image_path, "due to error:", e)
                continue

            max_confidence = get_max_confidence(resized_image)
            confidence_threshold = 0.6  # You can adjust this value
            if max_confidence < confidence_threshold:
                # Generate a unique filename for the shortcut
                shortcut_filename = f"{int(max_confidence * 100000):06d}_{index}." + image_path.split(".")[-1]
                shortcut_path = os.path.join(output_dir, shortcut_filename)

                # Create a shortcut to the original image (save space)
                os.link(image_path, shortcut_path)

                # Write the original path, shortcut path
                paths_file.write(f'{original_path}|{shortcut_path}\n')
                index += 1

    print("Images copied as shortcuts and paths recorded.")

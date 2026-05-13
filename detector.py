import argparse
import sys

import cv2
import numpy as np


def extract_image_center(image: np.ndarray, width: int, height: int) -> np.ndarray:
    img_height, img_width = image.shape[:2]
    start_x = img_width // 2 - width // 2
    start_y = img_height // 2 - height // 2
    return image[start_y:start_y + height, start_x:start_x + width]


def is_camera_obstructed(frame: np.ndarray, threshold=0.2) -> bool:
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    fft_shift = np.fft.fftshift(np.fft.fft2(grayscale_frame))
    spectrum_magnitude = 20 * np.log1p(np.abs(fft_shift))

    central_spectrum = extract_image_center(spectrum_magnitude,
                                            height=frame.shape[0] // 8,
                                            width=frame.shape[1] // 8)

    high_freq_ratio = np.count_nonzero(central_spectrum > 200) / central_spectrum.size
    print(f"ratio: {high_freq_ratio:.4f}")

    return high_freq_ratio < threshold


def check_camera(camera: int, threshold: float) -> bool:
    cap = cv2.VideoCapture(camera)
    if not cap.isOpened():
        print(f"Cannot open camera {camera}", file=sys.stderr)
        sys.exit(1)
    _, frame = cap.read()
    cap.release()
    return is_camera_obstructed(frame, threshold)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect physical camera obstruction")
    parser.add_argument("-c", "--camera", type=int, default=0, metavar="INDEX",
                        help="camera device index (default: 0)")
    parser.add_argument("-t", "--threshold", type=float, default=0.2, metavar="FLOAT",
                        help="high-frequency ratio threshold (default: 0.2)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    obstructed = check_camera(args.camera, args.threshold)
    print("Camera is Obstructed" if obstructed else "Camera is Unobstructed")
    sys.exit(2 if obstructed else 0)

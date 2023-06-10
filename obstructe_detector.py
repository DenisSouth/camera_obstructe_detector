import cv2
import numpy as np


def extract_image_center(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Extract the center of a given image.
    """
    img_height, img_width = image.shape[:2]
    start_x = img_width // 2 - width // 2
    start_y = img_height // 2 - height // 2
    return image[start_y:start_y + height, start_x:start_x + width]


def is_camera_obstructed(frame: np.ndarray, threshold=0.2, debug=False) -> bool:
    """
    Determine whether the camera is obstructed.
    """
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    fft_shift = np.fft.fftshift(np.fft.fft2(grayscale_frame))
    spectrum_magnitude = 20 * np.log1p(np.abs(fft_shift))

    central_spectrum = extract_image_center(spectrum_magnitude,
                                            height=frame.shape[0] // 8,
                                            width=frame.shape[1] // 8)

    high_freq_ratio = np.count_nonzero(central_spectrum > 200) / central_spectrum.size

    if debug:
        cv2.imshow("Frame", frame)
        cv2.imshow("Spectrum Magnitude", np.uint8(central_spectrum))
        print("High Frequency Ratio:", high_freq_ratio)
        cv2.waitKey(100)

    return high_freq_ratio < threshold


if __name__ == "__main__":
    video_feed = cv2.VideoCapture(0)
    while video_feed.isOpened():
        frame_read_successfully, current_frame = video_feed.read()
        camera_obstructed = is_camera_obstructed(current_frame, debug=False)

        print("Camera is Obstructed" if camera_obstructed else "Camera is Unobstructed")
    video_feed.release()
    cv2.destroyAllWindows()

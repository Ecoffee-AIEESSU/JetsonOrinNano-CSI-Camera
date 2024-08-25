import cv2
import os

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def get_next_filename(save_dir, base_name="plasticcup_image", extension=".jpg"):
    # Find the next available filename
    i = 1
    while True:
        filename = f"{base_name}{i}{extension}"
        file_path = os.path.join(save_dir, filename)
        if not os.path.isfile(file_path):
            return file_path
        i += 1

def show_camera(save_dir):
    window_title = "CSI Camera"

    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=2))  # flip_method=2 for vertical flip
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame = video_capture.read()
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)
                else:
                    break
                keyCode = cv2.waitKey(10) & 0xFF
                if keyCode == 27 or keyCode == ord('q'):
                    break
                if keyCode == ord('s'):
                    save_path = get_next_filename(save_dir)
                    cv2.imwrite(save_path, frame)
                    print(f"Image saved to {save_path}")
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")

if __name__ == "__main__":
    save_dir = "/home/aieessu/labelling" # 원하는 경로로 변경
    show_camera(save_dir)

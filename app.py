import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def detect_gesture(frame, gesture):
    # Convert frame and gesture to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_gesture = cv2.cvtColor(gesture, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(gray_frame, gray_gesture, cv2.TM_CCOEFF_NORMED)
    threshold = 0.5  # Adjust threshold as needed
    loc = np.where(result >= threshold)

    # Check if match is found
    if len(loc[0]) > 0:
        return True
    else:
        return False

def browse_image():
    global image_path
    image_path = filedialog.askopenfilename(title="Select Image")
    if image_path:
        image_label.config(text=f"Selected Image: {image_path}")

def browse_video():
    global video_path
    video_path = filedialog.askopenfilename(title="Select Video")
    if video_path:
        video_label.config(text=f"Selected Video: {video_path}")

def main():
    if not (image_path and video_path):
        return

    # Load gesture representation (image or video clip)
    gesture_representation = cv2.imread(image_path)  # Replace with your gesture representation

    # Read the test video
    cap = cv2.VideoCapture(video_path)  # Replace with your test video path

    # Get the width and height of the video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_video/output_video.avi', fourcc, 20.0, (width, height))

    # Create a resizable window
    cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Frame', width // 2, height // 2)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect gesture in the frame
        gesture_detected = detect_gesture(frame, gesture_representation)

        # If gesture is detected, overlay "DETECTED" text
        if gesture_detected:
            cv2.putText(frame, 'DETECTED', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 8, cv2.LINE_AA)

        # Write the frame to the output video
        out.write(frame)

        # Display the frame
        cv2.imshow('Frame', frame)

        # Quit the program if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and writer objects and close windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Create Tkinter GUI
root = tk.Tk()
root.title("Gesture Detection App")

# Browse buttons
browse_image_button = tk.Button(root, text="Browse Image", command=browse_image, width=20)
browse_image_button.pack(pady=10)

browse_video_button = tk.Button(root, text="Browse Video", command=browse_video, width=20)
browse_video_button.pack(pady=10)

start_button = tk.Button(root, text="Start Detection", command=main, width=20)
start_button.pack(pady=10)

image_label = tk.Label(root, text="Selected Image: None", width=50)
image_label.pack()

video_label = tk.Label(root, text="Selected Video: None", width=50)
video_label.pack()

image_path = ''
video_path = ''

root.mainloop()

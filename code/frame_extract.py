import cv2
from tkinter import messagebox
#-*-coding: utf-8-*-

def extract_frame():
    # Open the video file
    input_video_path = 'data/vehicle.mp4'
    output_image_path = 'temp/output_frame.jpg'
    frame_index = 5
    cap = cv2.VideoCapture(input_video_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        messagebox.showerror("Error", "Unable to open the video.")
        return

    # Move to the specified frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

    # Read the frame
    ret, frame = cap.read()

    # Check if the frame is read successfully
    if not ret:
        messagebox.showerror("Error", "Unable to read the frame.")
        return

    # Save the frame as an image
    cv2.imwrite(output_image_path, frame)

    # Close the video file
    cap.release()

    messagebox.showinfo("Extraction Complete", f"Frame extraction from the video successful.")

extract_frame()

# -*- coding: utf-8 -*-
import cv2
import sys
from tkinter import messagebox

def extract_frame():
    # Open the video file
    input_video_path = sys.argv[1]
    output_image_path = 'output_frame.jpg'
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

    messagebox.showinfo("Extraction Complete", "Frame extraction from the video successful.")

extract_frame()

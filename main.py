import tkinter as tk
from tkinter import filedialog
import subprocess
import os

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    if file_path:
        file_name = os.path.basename(file_path)
        print(file_name)
        run_program(file_name)

def run_program(file_name):
    try:
        subprocess.run(['python3', 'frame_extract.py',file_name])
    except FileNotFoundError:
        print("Unable to find the file 'frame_extract.py'.")
    try:
        subprocess.run(['python3', 'draw_area.py',file_name])
    except FileNotFoundError:
        print("Unable to find the file 'draw_area.py'.")
    try:
        subprocess.run(['python3', 'videotest.py',file_name])

    except FileNotFoundError:
        print("Unable to find the file 'videotest.py'.")
    root.destroy()

# Tkinter 창 생성
root = tk.Tk()
root.title("Video Processor")

# 파일 선택 버튼 생성
button = tk.Button(root, text="Select Video", command=open_file_dialog)
button.pack(pady=20)

# Tkinter 이벤트 루프 시작
root.mainloop()

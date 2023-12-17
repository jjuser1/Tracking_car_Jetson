# -*- coding: utf-8 -*-
import subprocess

def run_program():
    try:
        subprocess.run(['python', 'code/frame_extract.py'])
    except FileNotFoundError:
        print("Unable to find the file 'frame_extract.py'.")
    try:
        subprocess.run(['python', 'code/draw_area.py'])
    except FileNotFoundError:
        print("Unable to find the file 'draw_area.py'.")
    try:
        subprocess.run(['python', 'code/videotest.py'])
    except FileNotFoundError:
        print("Unable to find the file 'videotest.py'.")

run_program()

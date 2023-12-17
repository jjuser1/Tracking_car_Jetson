# -*- coding: utf-8 -*-
import cv2
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ultralytics import YOLO
from PIL import Image, ImageTk
import re

class VideoTrackerApp:
    def __init__(self, root, video_path):
        self.charge = {}
        self.paused = False
        self.user_text_1 = ""
        self.user_text_2 = ""
        self.txt_result = self.extract_coordinates_from_file()

        self.root = root
        self.root.title("Toll Booth CCTV Video")

        self.model = YOLO('data/best.pt')
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        self.setup_gui()

    def setup_gui(self):
        self.video_label = tk.Label(self.root)
        self.video_label.pack(side=tk.TOP)

        columns = ('Lane', 'Vehicle ID', 'Charge')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(side=tk.TOP)

        # Text box for instruction at the bottom left corner
        self.instruction_label = tk.Label(self.root, text=" 'P'\t: Play/Pause Video\n'Enter'\t: Enter Lane and Charge")
        self.instruction_label.pack(side=tk.BOTTOM, anchor=tk.SW)

        self.root.bind('<p>', self.toggle_pause_play)
        self.root.bind('<Return>', self.get_user_text)

        self.root.after(0, self.update)
        self.root.mainloop()

    def toggle_pause_play(self, event=None):
        self.paused = not self.paused

    def get_user_text(self, event=None):
        self.user_text_1 = simpledialog.askstring("Input", "Enter Lane")
        self.user_text_2 = simpledialog.askstring("Input", "Enter Charge")
        self.remove_charge_item()

    def remove_charge_item(self):
        if self.user_text_1 and self.user_text_2:
            try:
                lane_number = int(self.user_text_1)
                charge_value = int(self.user_text_2)
                for id, value in self.charge.items():
                    if value[0] == lane_number and value[1] == charge_value:
                        del self.charge[id]
                        message = "Settled {}won for Lane {}.".format(charge_value, lane_number)
                        messagebox.showinfo("Settled", message)
                        break
                else:
                    messagebox.showinfo("Vehicle Not Found", "Unable to find the specified vehicle.")
            except ValueError:
                messagebox.showerror("Error", "Please enter only numbers for Lane and Charge.")

    def update(self):
        if not self.paused:
            success, frame = self.cap.read()
            if success:
                results = self.model.track(frame, persist=True)
                detections = self.extract_detections(results)

                a = self.check_coordinates_against_ranges(detections, self.txt_result)
                self.tip(a)
                chargeitem = list(self.charge.items())
                data = [(str(int(det[1][0]))+"Lane", str(int(det[0]))+"th Vehicle", str(det[1][1])+"won") for det in chargeitem]

                self.populate_tree(data)

                img = Image.fromarray(cv2.cvtColor(results[0].plot(), cv2.COLOR_BGR2RGB))
                img = ImageTk.PhotoImage(image=img)
                self.video_label.img = img
                self.video_label.configure(image=img)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.quit()
            else:
                self.quit()

        self.root.after(1, self.update)

    def populate_tree(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in data:
            self.tree.insert('', 'end', values=row)

    def quit(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

    def extract_detections(self, results):
        detections = []
        confidence = results[0].boxes.conf.cpu().tolist()
        for i in range(len(results[0].boxes.xywh)):
            if confidence[i] >= 0.8:
                x, y, w, h = results[0].boxes.xywh[i].cpu().tolist()
                track_id = results[0].boxes.id[i].item()
                class_id = results[0].boxes.cls[i].item()

                mid_x = x
                mid_y = y + h/2

                detections.append([track_id, class_id, mid_x, mid_y])

        return detections

    def extract_coordinates_from_file(self):
        file_path = 'temp/area.txt'
        pattern = re.compile(r'\((\d+\.\d+), (\d+\.\d+)\)')
        selected_values_array = []

        with open(file_path, 'r') as file:
            for line in file:
                matches = pattern.findall(line)
                coordinates = [(float(x), float(y)) for x, y in matches]

                x_sorted = sorted(coordinates, key=lambda coord: coord[0])
                second_largest_x = x_sorted[-3][0]
                third_largest_x = x_sorted[-2][0]

                y_sorted = sorted(coordinates, key=lambda coord: coord[1])
                min_y = y_sorted[-3][1]
                max_y = y_sorted[-2][1]

                selected_values = (second_largest_x, third_largest_x, min_y, max_y)
                selected_values_array.append(selected_values)

        return selected_values_array

    def check_coordinates_against_ranges(self, coordinates_list, ranges):
        result = [0] * len(ranges)
        for id, cls, x, y in coordinates_list:
            j = 0
            for x2, x3, y2, y3 in ranges:
                if x2 <= x <= x3 and y2 <= y <= y3:
                    result[j] = [id, cls]
                j += 1

        return result

    def tip(self, result):
        i = 0
        for item in result:
            if item != 0:
                id = item[0]
                if id not in self.charge:
                    self.charge[id] = [i+1, self.check_tip(item[1])]
            i += 1
        return self.charge

    def check_tip(self, cls):
        charge_values = {0: 100, 1: 200, 2: 300, 3: 400, 4: 500, 5: 600}
        return charge_values.get(cls, 700)

if __name__ == "__main__":
    video_path = 'data/vehicle.mp4'
    root = tk.Tk()
    app = VideoTrackerApp(root, video_path)

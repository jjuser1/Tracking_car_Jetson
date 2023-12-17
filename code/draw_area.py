import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
#-*-coding: utf-8-*-

class ImageSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lane Area Configuration")

        self.image_path = None
        self.image = None
        self.photo_image = None
        self.example_image_path = 'data/example_image.jpg'  # Example image file path

        self.canvas = tk.Canvas(root)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.v_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.h_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Motion>", self.on_mouse_motion)
        self.root.bind("<Key-r>", self.delete_coordinates)
        self.root.bind("<Key-t>", self.save_coordinates)
        self.root.bind("<Key-q>", self.quit_app)

        self.root.bind("<w>", lambda event: self.scroll_canvas(-1, "y"))
        self.root.bind("<s>", lambda event: self.scroll_canvas(1, "y"))
        self.root.bind("<a>", lambda event: self.scroll_canvas(-1, "x"))
        self.root.bind("<d>", lambda event: self.scroll_canvas(1, "x"))

        self.points = []
        self.current_line_id = None
        self.polygon_coords = []
        self.polygon_ids = []

        self.text_widget = tk.Text(root, height=10, width=160)
        self.text_widget.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.guide_label = tk.Label(root, text="Left Click\t: Add coordinates to the area\nRight Click: Complete area configuration\n'r'\t: Delete the last saved area\n't'\t: Save area coordinates to a file\n'WSAD'\t: Scroll\n'q'\t: Quit",
                                    justify=tk.LEFT, anchor="nw", font=("Helvetica", 15), wraplength=400)
        self.guide_label.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.open_image()

    def open_image(self):
        file_path = 'temp/output_frame.jpg'
        if file_path:
            self.image_path = file_path
            self.load_images()

    def load_images(self):
        self.image = Image.open(self.image_path)
        self.example_image = Image.open(self.example_image_path)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.example_photo_image = ImageTk.PhotoImage(self.example_image)
        self.update_canvas_scrollregion()

    def update_canvas_scrollregion(self):
        if self.image:
            self.canvas.config(scrollregion=(0, 0, self.image.width + self.example_image.width, max(self.image.height, self.example_image.height)))
            
            # Draw the original image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
            
            # Draw the example image
            self.canvas.create_image(self.image.width+100, 0, anchor=tk.NW, image=self.example_photo_image)

    def on_mouse_click(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if self.current_line_id:
            self.canvas.delete(self.current_line_id)

        self.points.append((x, y))
        self.draw_polygon()

    def on_right_click(self, event):
        if len(self.points) > 2:
            self.polygon_ids.append(self.current_line_id)
            self.polygon_coords.append(self.points.copy())
            self.points = []
            self.current_line_id = None
            self.update_text_widget()

    def on_mouse_motion(self, event):
        if self.points:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            if self.current_line_id:
                self.canvas.delete(self.current_line_id)
            self.current_line_id = self.canvas.create_line(
                *sum(self.points[-1:], (x, y)),
                fill="red"
            )

    def draw_polygon(self):
        if len(self.points) > 1:
            if self.current_line_id:
                self.canvas.delete(self.current_line_id)
            self.current_line_id = self.canvas.create_polygon(
                *sum(self.points, ()),
                outline="blue",
                fill="",
                width=2
            )

    def update_text_widget(self):
        self.text_widget.delete(1.0, tk.END)
        for i, coords in enumerate(self.polygon_coords, start=1):
            self.text_widget.insert(tk.END, f"{i} Lane : {coords}\n")

    def delete_coordinates(self, event):
        if self.polygon_coords:
            last_polygon_id = self.polygon_ids.pop()
            self.canvas.delete(last_polygon_id)
            self.polygon_coords.pop()
            if self.points:
                self.canvas.delete(self.current_line_id)
                self.current_line_id = None

            self.update_text_widget()

    def quit_app(self, event):
        self.root.destroy()

    def scroll_canvas(self, amount, axis):
        if axis == "x":
            self.canvas.xview_scroll(amount, "units")
        elif axis == "y":
            self.canvas.yview_scroll(amount, "units")

    def save_coordinates(self, event):
        if self.polygon_coords:
            with open("temp/area.txt", "w") as file:
                for coords in self.polygon_coords:
                    file.write(" ".join(map(str, coords)) + "\n")
            messagebox.showinfo("Save Complete", "Area coordinates saved to the area.txt file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSelectorApp(root)
    root.mainloop()

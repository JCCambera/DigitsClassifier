import tkinter as Tk
from tkinter import ttk
import PIL
from PIL import Image, ImageDraw, ImageTk

import numpy as np
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_green = (255, 0, 0)

width_canvas = 400
height_canvas = 400

width_image_low_res = 28
height_image_low_res = 28

pen_width = 60

width_application = 600 * 2
height_application = 600 * 2

file_name_blank = "blank_img.png"
file_name = "number.png"
file_name_resized = "number_resized.png"


class MainWindow():
    def __init__(self, parent):
        # creation of the canvas
        self.root = parent

        self.canvas_1 = Tk.Canvas(self.root, width=width_canvas, height=height_canvas,relief='sunken')
        self.canvas_1.grid(row=0, column=0)

        # self.canvas_2 = Tk.Canvas(self.root, width=width_canvas, height=height_canvas)
        self.canvas_2 = Tk.Canvas(self.root, width=width_canvas, height=height_canvas,relief='sunken')
        self.canvas_2.grid(row=0, column=1)

        self.canvas_3 = Tk.Canvas(self.root, width=width_canvas, height=height_canvas, relief='sunken')
        self.canvas_3.grid(row=0, column=2)

        image_blank = ImageTk.PhotoImage(file=file_name_blank)

        self.img_label_canvas_2 = ttk.Label(self.canvas_2, image=image_blank)
        self.img_label_canvas_2.img_1 = image_blank
        self.img_label_canvas_2.config(compound = 'center')
        self.img_label_canvas_2.grid(row=0, column=0)

        self.img_label_canvas_3 = ttk.Label(self.canvas_3, image=image_blank, text='No classification',font = ('Courier',30,'bold'))
        self.img_label_canvas_3.img_1 = image_blank
        self.img_label_canvas_3.config(compound='center')
        self.img_label_canvas_3.grid(row=0, column=0)

        self.button_1 = Tk.Button(root, text="Save", command=self.on_btn1_save)
        self.button_1.grid(row=1, column=0)

        self.button_2 = Tk.Button(root, text="Preprocess", command=self.on_btn2_ld_preprocess_img)
        self.button_2.grid(row=1, column=1)

        self.button_3 = Tk.Button(root, text="Classify", command=self.on_btn3_classify)
        self.button_3.grid(row=1, column=2)

        # Drawing the number in the canvas
        self.mouse_lb_pressed = False # The mouse left button is not initially pressed
        self.drawingCoords = []
        self.canvas_1.bind("<B1-Motion>", self.on_moving_mouse)
        self.canvas_1.bind("<ButtonPress-1>", self.on_mouse_lb_pressed)
        self.canvas_1.bind("<ButtonRelease-1>", self.on_mouse_lb_released)

        # Saving the files in the

        self.image_2_save = Image.new("RGB", (width_canvas, height_canvas), color_white)

    def on_btn1_save(self):
        print('saving')
        image_2_save = Image.new("RGB", (width_canvas, height_canvas), color_white)
        draw_obj = ImageDraw.Draw(image_2_save)

        for point in self.drawingCoords:
            print(point)
            xy = [point[0] - pen_width / 2, point[1] - pen_width / 2, point[0] + pen_width / 2,
                point[1] + pen_width / 2]
            draw_obj.ellipse(xy, fill='black', outline=None)
        #
        draw_obj

        # saving the regular image
        image_2_save.save(file_name)

        # saving the scaled image
        image_2_save_resized = image_2_save.resize([width_image_low_res, height_image_low_res], PIL.Image.ANTIALIAS)
        image_2_save_resized.save(file_name_resized)



    def on_btn2_ld_preprocess_img(self):
        print('preprocessing')

        image_1 = Image.open(file_name_resized)
        image_1_resized = image_1.resize((width_canvas, height_canvas))
        photo_1 = ImageTk.PhotoImage(image_1_resized)

        self.img_label_canvas_2.config(image=photo_1)
        self.img_label_canvas_2.img_1 = photo_1

    def on_moving_mouse(self,event):
        # Ploting the draw into canvas 1
        if self.mouse_lb_pressed:
            self.canvas_1.create_oval(event.x - pen_width / 2, event.y - pen_width / 2, event.x + pen_width / 2,
                event.y + pen_width / 2, fill="black")
            self.drawingCoords.append((event.x, event.y))

    def on_mouse_lb_pressed(self,event):
        self.mouse_lb_pressed = True

    def on_mouse_lb_released(self,event):
        self.mouse_lb_pressed = False

    def on_btn3_classify(self):

        self.img_label_canvas_3.config(image=self.img_label_canvas_3.img_1)
        self.img_label_canvas_3.config(text='Classified')
                

root = Tk.Tk()
root.configure(background= 'gray')
MainWindow(root)
root.mainloop()
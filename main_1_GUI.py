from main_2_Classifier import *
from main_3_ImageProcessing import *

import tkinter as Tk
from tkinter import ttk
import PIL
from PIL import Image, ImageDraw, ImageTk

import os, random

# import numpy as np
# import matplotlib

# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt

color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_green = (255, 0, 0)

width_canvas = 400
height_canvas = 400

width_image_low_res = 28
height_image_low_res = 28

pen_width = 30

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

        self.canvas_2 = Tk.Canvas(self.root, width=width_canvas, height=height_canvas,relief='sunken')
        self.canvas_2.grid(row=0, column=1)

        self.canvas_3 = Tk.Canvas(self.root, width=width_canvas, height=height_canvas, relief='sunken')
        self.canvas_3.grid(row=0, column=2)

        image_blank = ImageTk.PhotoImage(file=file_name_blank)

        self.img_label_canvas_2 = ttk.Label(self.canvas_2, image=image_blank)
        self.img_label_canvas_2.img_1 = image_blank
        self.img_label_canvas_2.config(compound = 'center')
        self.img_label_canvas_2.grid(row=0, column=0)

        self.img_label_canvas_3 = ttk.Label(self.canvas_3, image=image_blank, text='No classification', font = ('Courier',30,'bold'))
        self.img_label_canvas_3.img_1 = image_blank
        self.img_label_canvas_3.config(compound='center')
        self.img_label_canvas_3.grid(row=0, column=0)

        self.button_1 = Tk.Button(root, text="Save", command=self.on_btn1_save)
        self.button_1.grid(row=1, column=0)

        self.button_2 = Tk.Button(root, text="Preprocess", command=self.on_btn2_ld_preprocess_img)
        self.button_2.grid(row=1, column=1)

        self.button_3 = Tk.Button(root, text="Classify", command=self.on_btn3_classify)
        self.button_3.grid(row=1, column=2)

        self.button_4 = Tk.Button(root, text="Load Random Image", command=self.on_btn4_ld_random_img)
        self.button_4.grid(row=2, column=1)

        # Drawing the number in the canvas
        self.mouse_lb_pressed = False # The mouse left button is not initially pressed
        self.drawingCoords = []
        self.canvas_1.bind("<B1-Motion>", self.on_moving_mouse)
        self.canvas_1.bind("<ButtonPress-1>", self.on_mouse_lb_pressed)
        self.canvas_1.bind("<ButtonRelease-1>", self.on_mouse_lb_released)

        # Saving the files in the
        self.image_2_save = Image.new("RGB", (width_canvas, height_canvas), color_white)

        # Create a digit classifier
        self.digitsClassifier = DigitsClassifier()
        self.digitsClassifier.printClassifierPerformance()

        # digitsClassifier.testRandomImage()
        # image_test_1 = digitsClassifier.getRandomImage()
        # print(type(image_test_1))
        # print(image_test_1.shape)

    def on_btn4_ld_random_img(self):
        # Cleaning the drawing (the points recorded are erased, and the canvas cleared)
        self.drawingCoords = []
        self.canvas_1.delete("all")
        file_name = random.choice(os.listdir("originalDB"))
        file_address = "originalDB" + '/' + file_name
        # print(file_address)
        PIL_image = ImageProcessing.load_Image_PIL_BW(file_address)
        NP_image = ImageProcessing.convert_PIL_2_NP(PIL_image)

        self.image_to_classify = NP_image

        # image_1 = Image.open(file_name_resized)
        # print("Type image: ", type(image_1))
        # image_1.load()
        # print("Type image: ", type(image_1))
        # image_1_resized = image_1.resize((width_canvas, height_canvas))
        # image_1_data_np = np.asarray(image_1_resized, dtype="int32")
        # print("Type data: ", type(image_1_data_np))
        # photo_1 = ImageTk.PhotoImage(image_1_resized)

        PIL_image_resized = PIL_image.resize((width_canvas, height_canvas))
        NP_image_resized = ImageProcessing.convert_PIL_2_NP(PIL_image_resized)
        TK_image_resized = ImageProcessing.convert_NP_2_TK(NP_image_resized)

        self.img_label_canvas_2.config(image=TK_image_resized)
        self.img_label_canvas_2.img_1 = TK_image_resized

        # self.image_to_classify.show()
        #  Loading a random image
        # self.digitsClassifier.classify_NP_image()

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

        # # saving the scaled image
        # image_2_save_resized = image_2_save.resize([width_image_low_res, height_image_low_res], PIL.Image.ANTIALIAS)
        # image_2_save_resized.save(file_name_resized)

    def canvas_2_load_image(self,np_image):
        #<Convert from numpy array to PIL image
         # Resize the image
         # Conver to TK image
         # To show in the canvas
        print("Hello")
    def loadImage_PIL(self,file_name):
        image_1 = Image.open(file_name_resized)
        image_1.load()
        image_1_resized = image_1.resize((width_canvas, height_canvas))
        image_1_data_np = np.asarray(image_1_resized, dtype="int32")
        
    def on_btn2_ld_preprocess_img(self):

        PIL_image = ImageProcessing.load_Image_PIL_BW(file_name)
        PIL_image_clc = ImageProcessing.trim_offset_PIL(PIL_image,0.3)
        PIL_image_clc_resized = PIL_image_clc.resize([width_image_low_res, height_image_low_res], PIL.Image.ANTIALIAS)
        PIL_image_clc_resized.save(file_name_resized)
        NP_image_clc_resized = ImageProcessing.convert_PIL_2_NP(PIL_image_clc_resized)
        PIL_image_clc_extended = PIL_image_clc_resized.resize([width_canvas,height_canvas])


        NP_image_clc_extended = ImageProcessing.convert_PIL_2_NP(PIL_image_clc_extended)
        TK_image_clc_extended = ImageProcessing.convert_NP_2_TK(NP_image_clc_extended)

        self.img_label_canvas_2.config(image=TK_image_clc_extended)
        self.img_label_canvas_2.img_1 = TK_image_clc_extended
        self.image_to_classify = NP_image_clc_resized

        # image_1 = Image.open(file_name_resized)
        # print("Type image: ",type(image_1))
        # image_1.load()
        # print("Type image: ", type(image_1))
        # image_1_resized = image_1.resize((width_canvas, height_canvas))
        # image_1_data_np = np.asarray(image_1_resized, dtype="int32")
        # print("Type data: ", type(image_1_data_np))
        # photo_1 = ImageTk.PhotoImage(image_1_resized)
        # self.image_to_classify = image_1_data_np




    def on_moving_mouse(self,event):
        # Plotting the draw into canvas 1
        if self.mouse_lb_pressed:
            self.canvas_1.create_oval(event.x - pen_width / 2, event.y - pen_width / 2, event.x + pen_width / 2,
                event.y + pen_width / 2, fill="black")
            self.drawingCoords.append((event.x, event.y))

    def on_mouse_lb_pressed(self,event):
        self.mouse_lb_pressed = True

    def on_mouse_lb_released(self,event):
        self.mouse_lb_pressed = False

    def on_btn3_classify(self):
        #print("file name resized: ",file_name_resized)

        # label_num = self.digitsClassifier.classifyImage(file_name_resized)
        # ImageProcessing.plot_NP_image(self.image_to_classify)
        label_num = self.digitsClassifier.classify_NP_image(self.image_to_classify)
        print("label identified: ", label_num)

        label_text = {
            1: 'ONE',
            2: 'TWO',
            3: 'THREE',
            4: 'FOUR',
            5: 'FIVE',
            6: 'SIX',
            7: 'SEVEN',
            8: 'EIGHT',
            9: 'NINE',
            0: 'ZERO',
        }.get(label_num, 'FAILED')
        self.img_label_canvas_3.config(text=label_text)
                

root = Tk.Tk()
root.configure(background= 'gray')
MainWindow(root)
root.mainloop()
from PIL import Image, ImageDraw, ImageTk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import tkinter as Tk
from tkinter import ttk



class ImageProcessing:

    @staticmethod
    def load_Image_PIL_BW(file_name):
        return Image.open(file_name).convert("L")

    @staticmethod
    def convert_PIL_2_NP(PIL_image):
        return np.array(PIL_image, dtype = np.uint8)

    @staticmethod
    def convert_NP_2_PIL(NP_image):
        PIL_image = Image.fromarray(NP_image, 'L')
        return PIL_image

    @staticmethod
    def save_PIL(PIL_image,file_name):
        PIL_image.save(file_name)

    @staticmethod
    def normalizeImages(NP_image,max_value):
        # Set the color image (black and white) to values between 0 and 255
        print("The maximum is:", NP_image.max())
        factor = np.uint8((max_value/NP_image.max()))
        print(type(NP_image[0][0]))
        NP_image = np.multiply(NP_image,factor)
        print(type(NP_image[0][0]))

        return NP_image

    @staticmethod
    def plot_NP_image(NP_image):
        plt.imshow(NP_image, cmap="gray")
        plt.show()

    @staticmethod
    def convert_NP_2_TK(NP_image):
        # It is necessary to declare the Tk canvas before using this function
        # NP_image = ImageProcessing.normalizeImages(NP_image, 1)
        # print(NP_image)
        # print(NP_image.shape)
        # ImageProcessing.plot_NP_image(NP_image)
        PIL_image = Image.fromarray(NP_image, 'L')
        print(type(PIL_image))
        # PIL_image.show()
        TK_image = ImageTk.PhotoImage(PIL_image)
        return TK_image

    @staticmethod
    def resize_NP_image(NP_image,width,height):
        PIL_image = Image.fromarray(NP_image, 'L')
        PIL_image_resize = PIL_image.resize((width, height))
        return np.array(PIL_image_resize)

    @staticmethod
    def flat_NP_image(NP_image):
        return np.reshape(NP_image,NP_image.shape[0]*NP_image.shape[1])




if __name__ == '__main__':
    print("Execution as main")
    PIL_image = ImageProcessing.load_Image_PIL_BW("number_resized.png")
    NP_image = ImageProcessing.convert_PIL_2_NP(PIL_image)
    # print(PIL_image)
    # print(NP_image.shape)
    # print(NP_image)
    NP_image = ImageProcessing.normalizeImages(NP_image, 255)
    NP_image = ImageProcessing.resize_NP_image(NP_image, 200, 200)
    # print(NP_image)
    # ImageProcessing.plot_NP_image(NP_image)
    root = Tk.Tk()
    TK_image = ImageProcessing.convert_NP_2_TK(NP_image)

    width_canvas = 400
    height_canvas = 400

    canvas_2 = Tk.Canvas(root, width=width_canvas, height=height_canvas, relief='sunken')
    canvas_2.grid(row=0, column=0)
    img_canvas = canvas_2.create_image(200, 200,  image=TK_image)
    root.configure(background='gray')
    root.mainloop()

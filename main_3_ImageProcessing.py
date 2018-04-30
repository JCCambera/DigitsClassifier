from PIL import Image, ImageDraw, ImageTk, ImageChops
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

    @staticmethod
    def crop_PIL_image(PIL_image):
        bg = Image.new(PIL_image.mode, PIL_image.size, PIL_image.getpixel((0, 0)))
        diff = ImageChops.difference(PIL_image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        print(bbox)
        if bbox:
            return PIL_image.crop(bbox)
        else:
            return PIL_image

    @staticmethod
    def trim_offset_PIL(PIL_image, percentual_offset):
        bg = Image.new(PIL_image.mode, PIL_image.size, PIL_image.getpixel((0, 0)))
        diff = ImageChops.difference(PIL_image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        width = bbox[2]-bbox[0]
        height = bbox[3] - bbox[1]
        # Defining a blank image
        max_length_img = max(width,height)
        new_length_img =  int((percentual_offset+1)*max_length_img)
        print('max_length_img: ',max_length_img," new_length_img: ",new_length_img)
        new_im = Image.new("L", (new_length_img,new_length_img),"white")  ## luckily, this is already black!
        x_paste_pixel = int((new_length_img - width) / 2)
        y_paste_pixel =int((new_length_img- height)/2.0)


        print('x_paste_pixel: ',x_paste_pixel,' y_paste_pixel:',y_paste_pixel)


        print('width: ',width,' height:',height)

        PIL_img_cropped = PIL_image.crop(bbox)
        # new_im.show()
        # PIL_img_cropped.show()
        print('before:',new_im)
        print('before:', PIL_img_cropped)
        new_im.paste(PIL_img_cropped,(x_paste_pixel,y_paste_pixel))
        # new_im.paste(new_im, (0,0))

        print('after:', new_im)
        return new_im


if __name__ == '__main__':
    print("Execution as main")
    # PIL_image = ImageProcessing.load_Image_PIL_BW("number_resized.png")
    PIL_image = ImageProcessing.load_Image_PIL_BW("number.png")
    PIL_image.show()
    # PIL_image_cropped = ImageProcessing.crop_PIL_image(PIL_image)
    # PIL_image_cropped.show()

    PIL_image_cropped_2 = ImageProcessing.trim_offset_PIL(PIL_image, 0.30)
    # ImageProcessing.trim_offset_PIL(PIL_image, 0, 0)
    PIL_image_cropped_2.show()
    # NP_image = ImageProcessing.convert_PIL_2_NP(PIL_image)
    # # print(PIL_image)
    # # print(NP_image.shape)
    # # print(NP_image)
    # NP_image = ImageProcessing.normalizeImages(NP_image, 255)
    # NP_image = ImageProcessing.resize_NP_image(NP_image, 200, 200)
    # # print(NP_image)
    # # ImageProcessing.plot_NP_image(NP_image)
    # root = Tk.Tk()
    # TK_image = ImageProcessing.convert_NP_2_TK(NP_image)
    #
    # width_canvas = 400
    # height_canvas = 400
    #
    # canvas_2 = Tk.Canvas(root, width=width_canvas, height=height_canvas, relief='sunken')
    # canvas_2.grid(row=0, column=0)
    # img_canvas = canvas_2.create_image(200, 200,  image=TK_image)
    # root.configure(background='gray')
    # root.mainloop()

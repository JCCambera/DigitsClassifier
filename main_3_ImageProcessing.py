from PIL import Image, ImageDraw, ImageTk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt




class ImageProcessing:

    @staticmethod
    def load_Image_PIL_BW(file_name):
        image_1 = Image.open(file_name)
        image_1.load()
        image_1 = image_1.convert('1')  # convert image to black and white
        return image_1

    @staticmethod
    def convert_PIL_2_NP(PIL_image):
        return  np.asarray(PIL_image, dtype="int32")

    @staticmethod
    def normalizeImages(NP_image,max_value):
        # Set the color image (black and white) to values between 0 and 255
        NP_image = NP_image*(max_value/NP_image.max())
        return NP_image

    @staticmethod
    def plot_NP_image(NP_image):
        plt.imshow(NP_image, cmap="gray")
        plt.show()

    @staticmethod
    def convert_NP_2_TK(NP_image):
        # TODO: Probably it has to be with the meaning of what is black and white
        # NP_image = ImageProcessing.normalizeImages(NP_image, 1)
        print(NP_image)
        # ImageProcessing.plot_NP_image(NP_image)
        PIL_image = Image.fromarray(NP_image,'L')
        PIL_image.show()

        # PIL_image = Image.open("number_resized.png").convert("L")
        # # PIL_image.show()
        # NP_image = np.array(PIL_image)
        # print(NP_image)
        # print(NP_image.shape)
        # PIL_image = Image.fromarray(NP_image, 'L')
        # PIL_image.show()




if __name__ == '__main__':
    print("Execution as main")
    PIL_image = ImageProcessing.load_Image_PIL_BW("number_resized.png")
    NP_image = ImageProcessing.convert_PIL_2_NP(PIL_image)
    # print(PIL_image)
    # print(NP_image.shape)
    # print(NP_image)
    NP_image = ImageProcessing.normalizeImages(NP_image,255)
    # print(NP_image)
    # ImageProcessing.plot_NP_image(NP_image)
    ImageProcessing.convert_NP_2_TK(NP_image)

# TODO To lower the reesolution of the data set and save it into a file (Create a class to do this), it also should normalize, and convert it to  no array to be accepted by Sklearn
# TODO To configure the class in this file to accept as input the data set generated from the previous class

from mnist import MNIST
from math import sqrt
import random
from sklearn import datasets, svm, metrics
import numpy as np
from PIL import Image, ImageDraw, ImageTk
# import matplotlib.pyplot as plt
from main_3_ImageProcessing import *

class DigitsClassifier:
    def __init__(self):

        self.training_set_length = 3000
        self.test_set_length = 200

        # self.load_DigitsData_ScikitLearn()
        self.load_DigitsTrainningData()
        self.classifierDef_SVM(self.training_set_length)

    def load_DigitsData_ScikitLearn(self):
        digits = datasets.load_digits()

        self.images_training = digits.images[:self.training_set_length]
        self.labels_training = digits.target[:self.training_set_length]
        self.images_testing = digits.images[self.training_set_length+1:self.training_set_length+self.test_set_length+1]
        self.labels_testing = digits.target[self.training_set_length+1:self.training_set_length+self.test_set_length+1]

        # Flat versions of the images
        self.images_training_flatted = np.reshape(self.images_training, [self.images_training.shape[0],
                                                                         self.images_training.shape[1] *
                                                                         self.images_training.shape[2]])

        self.images_testing_flatted = np.reshape(self.images_testing, [self.images_testing.shape[0],
                                                                       self.images_testing.shape[1] *
                                                                       self.images_testing.shape[2]])

        # Adjusting images to the format black number, white background with ui8
        self.images_training_flatted = np.uint8(self.images_training_flatted)
        self.images_testing_flatted = np.uint8(self.images_testing_flatted)
        self.images_training = np.uint8(self.images_training)
        self.images_testing = np.uint8(self.images_testing)

                

    def load_DigitsTrainningData(self):
        # Loads the MINST Digits Data. The images come flatted

        mndata = MNIST()
        self.images_training_flatted, self.labels_training = mndata.load_training()
        self.images_testing_flatted, self.labels_testing = mndata.load_testing()



        # Definition of numpy arrays
        # self.images_training = np.array(self.images_training[:self.training_set_length])
        self.images_training_flatted = np.array(self.images_training_flatted[:self.training_set_length])
        self.labels_training = np.array(self.labels_training[:self.training_set_length])

        # self.images_testing = np.array(self.images_testing[:self.test_set_length])
        self.images_testing_flatted = np.array(self.images_testing_flatted[:self.test_set_length])
        self.labels_testing = np.array(self.labels_testing[:self.test_set_length])

        self.images_training_flatted = self.normalizeImages(self.images_training_flatted)
        self.images_testing_flatted = self.normalizeImages(self.images_testing_flatted)


        # print(self.images_training_flatted.shape)
        # print(self.images_testing_flatted.shape)

        # Definition of the flatten versions
        height_width_image_set = round(sqrt(self.images_training_flatted.shape[1]))
        length_training_set = self.images_training_flatted.shape[0]
        length_testing_set = self.images_testing_flatted.shape[0]
        # print('Here')
        # print(height_width_image_set)
        # print(length_training_set)
        # print(length_testing_set )


        self.images_training = np.reshape(self.images_training_flatted, [length_training_set,height_width_image_set,height_width_image_set])
        self.images_testing  = np.reshape(self.images_testing_flatted,[length_testing_set, height_width_image_set, height_width_image_set])

    def normalizeImages(self, image_NP_Array):
        # Set the color image (black and white) to values between 0 and 255
        for i in range(image_NP_Array.shape[0]):
            image_NP_Array[i, :] = image_NP_Array[i, :]*(255.0/image_NP_Array[i, :].max())
        return image_NP_Array

    def classifierDef_SVM(self,training_set_length):
        # Creates a classifier based on Support Vector Machine Algorithm

        self.classifier_svm = svm.SVC(gamma=0.0000001)
        # self.classifier_svm = svm.SVC(gamma=0.0000001) #Working
        self.classifier_svm.fit(self.images_training_flatted, self.labels_training)


    def printClassifierPerformance(self):

        training_labels_predicted = self.classifier_svm.predict(self.images_training_flatted)
        testing_labels_predicted = self.classifier_svm.predict(self.images_testing_flatted)
        training_accuracy = metrics.accuracy_score(self.labels_training, training_labels_predicted)
        testing_accuracy = metrics.accuracy_score(self.labels_testing, testing_labels_predicted)
        print('Classifier Accuracy in Training Set:',training_accuracy)
        print('Classifier Accuracy in Test Set:',testing_accuracy)
        
    def classify_SVM(self,image):
        return self.classifier_svm.predict([image])[0]

    def testRandomImage(self):
        idx_random = random.randint(0,self.test_set_length)
        image_test_flatted = self.images_testing_flatted[idx_random]
        print('DB type:',type(image_test_flatted[0]))
        print('DB max:', image_test_flatted.max())
        print('DB flatted shape:', image_test_flatted.shape)
        label_test = self.labels_testing[idx_random]
        label_id = self.classify_SVM(image_test_flatted)
        print('Label expected:  '+str(label_test) +', Label identified: '+str(label_id))
        # print('Max Value', image_test_flatted.max())
        # print(image_test_flatted)                                       º
    def getRandomImage(self):
        idx_random = random.randint(0, self.test_set_length)
        # return self.images_testing_flatted[idx_random]
        return self.images_testing[idx_random]

    def loadImage(self,file_name):
            img = Image.open(file_name)
            img.load()
            img = img.convert('L')  # convert image to monochrome
            img.show()
            data = np.asarray(img, dtype="int64")

            return data

    def flattenImage(self,image):
        return np.reshape(image,image.shape[0]*image.shape[1])

    def classifyImage(self,file_name):

        PIL_image = ImageProcessing.load_Image_PIL_BW(file_name)
        PIL_image.show()
        NP_image = ImageProcessing.convert_PIL_2_NP(PIL_image)
        NP_image = np.invert(NP_image)
        NP_image_flat = ImageProcessing.flat_NP_image(NP_image)

        # NP_image = self.getRandomImage()
        # NP_image_flat = ImageProcessing.flat_NP_image(NP_image)
        # ImageProcessing.plot_NP_image(NP_image)
        #

        # print('FILE Type:', type(NP_image_flat[0]))
        # print('FILE max:', NP_image_flat.max())
        # print('FILE flatted shape:', NP_image_flat.shape)
        # print('FILE shape:', NP_image.shape)
        # print(NP_image_flat)
        label_id = self.classify_SVM(NP_image_flat)
        # print('Label identified: ' + str(label_id))
        # print(flatted_image)
        return label_id

    def saveRandomImage(self):

        idx_random = random.randint(0,self.test_set_length)
        NP_image = self.images_testing[idx_random]
        NP_image = np.uint8(NP_image)
        NP_image =  np.invert(NP_image)
        # NP_image =  np.invert(NP_image, dtype= np.int64)

        ImageProcessing.plot_NP_image(NP_image)
        print(NP_image)
        print('PIL_2_NP:',NP_image.shape)
        print('PIL_2_NP:',type(NP_image[0][0]))
        print('PIL_2_NP:',NP_image.max())
        PIL_image = ImageProcessing.convert_NP_2_PIL(NP_image)
        PIL_image.show()
        ImageProcessing.save_PIL(PIL_image,'image_test.png')


if __name__ == '__main__':
    digitsClassifier = DigitsClassifier()
    # digitsClassifier.classifyImage("number_resized.png")
    # digitsClassifier.saveRandomImage()
    # digitsClassifier.classifyImage("image_test.png")
    # digitsClassifier.classifyImage("test_2_draw.png")
    # digitsClassifier.classifyImage("test_5_draw.png")
    # digitsClassifier.classifyImage("test_8_draw.png")
    # digitsClassifier.testRandomImage()



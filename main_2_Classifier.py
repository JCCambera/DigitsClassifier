# TODO To lower the reesolution of the data set and save it into a file (Create a class to do this), it also should normalize, and convert it to  no array to be accepted by Sklearn
# TODO To configure the class in this file to accept as input the data set generated from the previous class

from mnist import MNIST
from math import sqrt
import random
from sklearn import datasets, svm, metrics
import numpy as np
from PIL import Image, ImageDraw, ImageTk
import matplotlib.pyplot as plt


class DigitsClassifier:
    def __init__(self):

        self.training_set_length = 600
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

        #self.classifier_svm = svm.SVC(gamma=0.0000001)
        # self.classifier_svm = svm.SVC(gamma=0.0000001) #Working
        self.classifier_svm.fit(self.images_training_flatted, self.labels_training)

    def classify_SVM(self,image):
        return self.classifier_svm.predict([image])[0]

    def testRandomImage(self):
        idx_random = random.randint(0,self.test_set_length)
        image_test_flatted = self.images_testing_flatted[idx_random]
        label_test = self.labels_testing[idx_random]
        label_id = self.classify_SVM(image_test_flatted)
        print('Label expected:  '+str(label_test) +', Label identified: '+str(label_id))
        print('Max Value', image_test_flatted.max())
        # print(image_test_flatted)

    def loadImage(self,file_name):
            img = Image.open(file_name)
            img.load()
            img = img.convert('L')  # convert image to monochrome - this works
            img = img.convert('1')  # convert image to black and white
            img.show()
            data = np.asarray(img, dtype="int32")
            return data

    def flattenImage(self,image):
        return np.reshape(image,image.shape[0]*image.shape[1])
    def classifyImage(self,file_name):

        image = self.loadImage(file_name)
        print('Tipo')
        print(type(image))
        normalize_image = self.normalizeImages(image)
        flatted_image = self.flattenImage(normalize_image)
        print(normalize_image.shape)
        print(flatted_image.shape)
        label_id = self.classify_SVM(flatted_image)
        # plt.imshow(normalize_image, cmap="gray")
        # plt.show()

        print('Label identified: ' + str(label_id))
        print(flatted_image)



digitsClassifier = DigitsClassifier()
digitsClassifier.classifyImage("number_resized.png")
digitsClassifier.testRandomImage()

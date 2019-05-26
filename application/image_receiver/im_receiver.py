import logging
from PIL import Image
import numpy as np
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import unireedsolomon as rs
import bchlib
import hashlib
import random


class Receiver:

    """Uruchamia logi"""
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Receiver created")
        self.img = None
        self.numpy_img = None
        self.numpy_flat_img = None
        self.bytearray_img = None

    """Zapisuje otrzymany obraz w postaci numpy array"""
    def receive_img_as_np_array(self, imageAsNumpyArray):
        logging.debug("Receiver: Otrzmano obraz w Receiverze")
        self.numpy_flat_img = imageAsNumpyArray

    """Zapisuje otrzymany obraz w postaci bytearray"""
    def receive(self, bytearray_img):
        logging.debug("Receiver: Otrzmano obraz")
        self.bytearray_img = bytearray_img

    """Koweruje numpy array do typu Image zeby mozna bylo wyswietlac"""
    def convert_numpy_array_to_image(self):
        logging.debug("Receiver: Konwersja npyArray do Image w Receiverze")
        logging.debug(self.numpy_img.shape)
        self.img = Image.fromarray(self.numpy_img)

    """Konwertuje bytearray do typu Image"""
    def convert_bytearray_to_image(self, mode, size):
        logging.debug("Receiver: Konwersja npyArray do Image w Receiverze")
        logging.debug(self.numpy_img.shape)
        self.img = Image.frombytes(mode, size, bytes(self.bytearray_img))

    '''pokazuje obraz (nalezy go wczesniej skonwertowac metodą convertNpyArrayToImage)'''
    def show(self):
        logging.debug("Receiver: Wyświetlenie obrazu ")
        self.img.show()

    def reed_solomon_decode(self):
        logging.debug("Receiver: Dekodowanie Reeda Solomona")
        coder = rs.RSCoder(255, 223)
        input = self.numpy_flat_img

        output = []
        logging.debug("Receiver: Input")
        logging.debug(input)
        for data in input:
           # print("Data: ")
            #print(data)
            output.append(coder.decode(data)[0])
            #print("Encoded Data: ")
            #print(coder.decode(data))

        self.numpy_flat_img = np.array(output[0].split(" "))
        #self.numpy_flat_img = np.array(output)
        print(self.numpy_flat_img)


    def bch_decode(self): #TO DO
        logging.debug("Receiver: Dekodowanie BCH")
        self.BCH_POLYNOMIAL = 8219
        self.BCH_BITS = 17
        self.bch = bchlib.BCH(self.BCH_POLYNOMIAL, self.BCH_BITS)
        #print(len(self.numpyFlatImg))
        #self.numpyFlatImg= bytearray(self.numpyFlatImg)
        self.numpy_flat_img, self.ecc = self.numpy_flat_img[3:-self.bch.ecc_bytes], self.numpy_flat_img[-self.bch.ecc_bytes:]

        #self.ecc= bytearray(self.ecc)
        #self.ecc= self.ecc[::8]

        #self.numpyFlatImg= bytearray(self.numpyFlatImg)

        self.bch.decode(self.numpy_flat_img, self.ecc)

    def triple_decode(self):
        logging.debug("Receiver: Dekodowanie potrojonych bitów")

        output = []
        print(len(self.numpy_flat_img))

        for i in range(0,len(self.numpy_flat_img),3):
            if(i == len(self.numpy_flat_img)):
                break

            print(i)
            if(self.numpy_flat_img[i] == self.numpy_flat_img[i+1] or self.numpy_flat_img[i] == self.numpy_flat_img[i+2] ):
                output.append(self.numpy_flat_img[i])
            elif(self.numpy_flat_img[i+1] == self.numpy_flat_img[i+2]):
                output.append(self.numpy_flat_img[i+1])
            else:
                output.append(self.numpy_flat_img[i])

        self.numpy_flat_img = np.array(output)
        print(self.numpy_flat_img)


    """Przywracanie kształtów"""
    def reshape(self):
        logging.debug("Receiver: Przywracanie kształtów ")
        first_dim = self.numpy_flat_img[0]
        second_dim = self.numpy_flat_img[1]
        third_dim = self.numpy_flat_img[2]
        size = int(first_dim) * int(second_dim) * int(third_dim)
        
        self.numpy_img = [self.numpy_flat_img[3:size + 3]]
        self.numpy_img = np.array(self.numpy_img)
        self.numpy_img = self.numpy_img.transpose()
        self.numpy_img = np.squeeze(self.numpy_img, axis=1)

    def flat_array(self):
        logging.debug("Receiver: Prostowanie tablicy")
        firs_dim = len(self.numpy_img)
        second_dim = len(self.numpy_img[0])
        third_dim = len(self.numpy_img[0][0])
        self.numpy_flat_img = np.zeros(0)
        self.numpy_flat_img += firs_dim
        self.numpy_flat_img += second_dim
        self.numpy_flat_img += third_dim
        np.concatenate((self.numpy_flat_img, self.numpy_img.flatten()), axis=0)
        self.numpy_img = np.reshape(self.numpy_img, (firs_dim, second_dim, third_dim))

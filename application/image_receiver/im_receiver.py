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
  
        self.bch_numpy_img = None
        self.bch_numpy_flat_img = None
        self.size= None
        self.bch_first_dir= None
        self.bch_second_dir= None
        self.bch_third_dir= None
        self.title = 'Obraz odebrany'

    """Zapisuje otrzymany obraz w postaci numpy array"""
    def receive_img_as_np_array(self, imageAsNumpyArray):
        logging.debug("Receiver: Otrzymano obraz w Receiverze")
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
        self.img.show(title=self.title)

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

    def bch_receive(self, NoisyImg, size_x, size_y, size_z):
        logging.debug("RECEIVER		Otrzmano obraz w Receiverze")
        self.bch_numpy_flat_img= NoisyImg
        self.bch_first_dir=size_x
        self.bch_second_dir=size_y
        self.bch_third_dir=size_z
        self.size=self.bch_first_dir*self.bch_second_dir*self.bch_third_dir
 
    def bch_deboundling(self):
        logging.debug("RECEIVER		Dekodowanie BCH")
        self.BCH_POLYNOMIAL = 8219
        self.BCH_BITS = 123
        depacket = bytearray()
        bitflips = int()
        self.bch = bchlib.BCH(self.BCH_POLYNOMIAL, self.BCH_BITS)
        for x in range(0, int(len(self.bch_numpy_flat_img)/712)):
                bitflips += self.bch.decode_inplace(self.bch_numpy_flat_img[712*x:712*x+512], self.bch_numpy_flat_img[712*x+512:712*(x+1)])
        print('bitflips: %d' % (bitflips))
        for x in range(0, int(len(self.bch_numpy_flat_img)/712)):
            depacket = depacket+self.bch_numpy_flat_img[712*x:712*x+512]
        self.bch_numpy_flat_img = depacket

    def bch_to_num_array(self):
        logging.debug("RECEIVER		BCH TO NUMPY ARRAY")
        self.bch_numpy_flat_img = np.frombuffer(self.bch_numpy_flat_img[:self.size], dtype=np.uint8)

    def bch_reshape(self):
        logging.debug("RECEIVER		Przywracanie kształtów przez channel")
        self.bch_numpy_img = np.reshape(self.bch_numpy_flat_img.transpose(), (self.bch_first_dir, self.bch_second_dir, self.bch_third_dir))

    def bch_convert_npy_array_to_image(self):
        logging.debug("RECEIVER		Konwersja npyArray do Image w Receiverze")
        logging.debug(self.bch_numpy_img.shape)
        self.img = Image.fromarray(self.bch_numpy_img)

    def show(self):
        logging.debug("RECEIVER		Wyświetlenie obrazu w receiverze")
        self.img.show()

    def triple_decode(self):
        logging.debug("Receiver: Dekodowanie potrojonych bitów")

        output = []
        print(len(self.numpy_flat_img))

        for i in range(0, len(self.numpy_flat_img), 3):
            if i == len(self.numpy_flat_img):
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

    def reshape(self, shape):
        self.numpy_img = np.reshape(self.numpy_flat_img, shape)

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

from PIL import Image
import numpy as np
import logging
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import unireedsolomon as rs
import bchlib
import random


class Sender:

    """Inicjalizuje logging w trybie debug"""
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Sender created")
        self.img = None
        self.numpy_img = None
        self.numpy_flat_img = None
        self.bytearray_img = None

    """Laduje orazek z folderu  resources"""
    def load_picture(self):
        logging.debug("Sender: Your working directory is "+os.getcwd())
        os.chdir(r'./application/resources')
        Tk().withdraw() 
        filename = askopenfilename() 
        logging.debug("Sender: You choosed  "+filename)

        self.img = Image.open(filename)
        self.img.load()

    """Konwertuje objekt Image na tablicę numpy"""
    def converting_to_numpy_array(self):
        logging.debug("Sender: Konwersja obrazka do numpy array")
        self.numpy_img = np.array(self.img)

    """Konwertuje obiekt Image do bytearray"""
    def convert_img_to_bytearray(self):
        logging.debug("Sender: Konwersja obrazu do bytearray")
        self.bytearray_img = bytearray(self.img.tobytes())

    """Pokazuje obraz jaki został wczytany tzn przed zakłóceniami wprowadzonymi przez kanał transmisji"""
    def show(self):
        logging.debug("Sender: Wyswietlenie obrazka")
        self.img.show() 

    def send(self):
        logging.debug("Sender: Wysylanie obrazka")
        return self.numpy_flat_img

    def flat_array(self):
        logging.debug("Sender: Prostowanie tablicy")
        firstDir= len(self.numpy_img)
        secondDir= len(self.numpy_img[0])
        thirdDir= len(self.numpy_img[0][0])
        self.numpy_flat_img=np.array([firstDir, secondDir, thirdDir])
        self.numpy_flat_img= np.concatenate((self.numpy_flat_img, self.numpy_img.flatten()), axis= None)

    def reed_solomon_encode(self): #TO DO
        logging.debug("Sender: Kodowanie reeda solomona")
        coder = rs.RSCoder(255,223)
       # self.numpyImg = coder.encode(self.numpyImg)
        k = 223
        #self.ecc = coder.encode(self.numpyFlatImg)
        #self.packet= np.concatenate((self.numpyFlatImg, self.ecc), axis= None)
        #self.numpyFlatImg=self.packet

    def bch_encode(self): #TO DO
        logging.debug("Sender: Kodowanie BCH")
        self.BCH_POLYNOMIAL = 8219
        self.BCH_BITS = 17
        self.bch = bchlib.BCH(self.BCH_POLYNOMIAL, self.BCH_BITS)
        #self.data = bytearray(self.numpyFlatImg)
        # encode and make a "packet"
        self.ecc = self.bch.encode(self.numpy_flat_img)
        self.packet= np.concatenate((self.numpy_flat_img, self.ecc), axis= None)
        self.numpy_flat_img=self.packet


# to nizej to sprawdenie  czy wszystko działa
'''
s = Sender()
s.loadPicture()
s.convertImgToNumpyArray()
s.show()
'''

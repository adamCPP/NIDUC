from PIL import Image
import numpy as np
import logging
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import unireedsolomon as rs
import bchlib
import random
import math
import textwrap


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

    def reed_solomon_encode(self): 

        logging.debug("Sender: Kodowanie reeda solomona")
        #self.numpy_flat_img = np.array(self.numpy_flat_img[0:1000])
        coder = rs.RSCoder(255,223)
        output = []
        logging.debug("Sender: Numpy flat image")
        logging.debug(self.numpy_flat_img)
        logging.debug(self.numpy_flat_img.shape)
    
        print("Dlugosc stringa"+str(len(self.numpy_flat_img)))
        s=""
        s =  s + str(self.numpy_flat_img[0])
        for i in range(1,self.numpy_flat_img.shape[0]):
            s=s+" "+str(self.numpy_flat_img[i])


        self.numpy_flat_img = s

        logging.debug("Sender: Numpy string")
        print(self.numpy_flat_img)
        
        blocks = textwrap.wrap(self.numpy_flat_img,223)
        for block in blocks:
            code = coder.encode(block)
            logging.debug("block")
            logging.debug(block)
            output.append(code)
        self.numpy_flat_img=np.array(output)
        logging.debug("Sender: output shape")
        logging.debug(self.numpy_flat_img.shape)
        logging.debug("Sender: output ")
        logging.debug(self.numpy_flat_img[0])
	
    def BCH_encode(self): #TO DO
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

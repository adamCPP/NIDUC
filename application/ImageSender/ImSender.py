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

    
    ''' Inicjalizuje logging w trybie debug'''
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Sender created")
        self.img = None
        self.numpyImg = None
        self.numpyFlatImg = None


    '''Laduje orazek z folderu  resources'''
    def loadPicture(self):
        logging.debug("Your working directory is "+os.getcwd())
        os.chdir(r'./application/resources')
        Tk().withdraw() 
        filename = askopenfilename() 
        logging.debug("You choosed  "+filename)

        self.img = Image.open(filename)
        self.img.load()

    '''Konwertuje objekt Image na tablicę numpy'''
    def convertImgToNumpyArray(self):
        logging.debug("Konwersja obrazka do numpy array")
        self.numpyImg = np.array(self.img)

	

    '''Pokazuje obraz jaki został wczytany tzn przed zakłóceniami wprowadzonymi przez kanał transmisji'''
    def show(self):
        logging.debug("Wyswietlenie obrazka")
        self.img.show() 


    def send(self):
        logging.debug("Wysylanie obrazka")
        
        self.BCHEncode()
        return self.numpyImg

    def floatArray(self):
        logging.debug("Prostowanie tablicy")
        firstD= len(self.numpyImg)
        secondD= len(self.numpyImg[0]) 
        thirdD= len(self.numpyImg[0][0])
        self.numpyFlatImg=np.zeros(5)
        self.numpyFlatImg+=firstD
        self.numpyFlatImg+=secondD
        self.numpyFlatImg+=thirdD
        np.concatenate((self.numpyFlatImg, self.numpyImg.flatten()), axis=0)
        #self.numpyFlatImg+=self.numpyImg.flatten()

    def reedSolomonEncode(self): #TO DO
        logging.debug("Kodowanie reeda solomona")
        coder = rs.RSCoder(255,223)
       # self.numpyImg = coder.encode(self.numpyImg)
	
    def BCHEncode(self): #TO DO
        logging.debug("Kodowanie BCH")
        self.floatArray()
        self.BCH_POLYNOMIAL = 8219
        self.BCH_BITS = 17
        self.bch = bchlib.BCH(self.BCH_POLYNOMIAL, self.BCH_BITS)
        self.data = self.numpyFlatImg
        # encode and make a "packet"
        self.ecc = self.bch.encode(self.data)
        self.packet = np.concatenate((self.data, self.ecc), axis=0)
        self.numpyFlatImg=self.packet

        

# to nizej to sprawdenie  czy wszystko działa
'''
s = Sender()
s.loadPicture()
s.convertImgToNumpyArray()
s.show()
'''

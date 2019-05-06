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

    
    ''' uruchamia logi'''
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Receiver created")
        self.img = None
        self.numpyImg = None
        self.numpyFlatImg = None

    '''zapisuje otrzymany obraz w postaci numpy array'''
    def receive(self,imageAsNumpyArray):
        logging.debug("Otrzmano obraz w Receiverze")
        self.numpyFlatImg = imageAsNumpyArray


    ''' koweruje numpy array do typu Image zeby mozna bylo wyswietlac'''
    def convertNpyArrayToImage(self):
        logging.debug("Konwersja npyArray do Image w Receiverze")
        logging.debug(self.numpyImg.shape)
        self.img = Image.fromarray(self.numpyImg)

    '''pokazuje obraz (nalezy go wczesniej skonwertowac metodą convertNpyArrayToImage)'''
    def show(self):
        logging.debug("Wyświetlenie obrazu w receiverze")
        self.img.show()

    def reedSolomonDecode(self):
        logging.debug("Dekodowanie Reeda Solomona")
        coder = rs.RSCoder(255,223)
        self.numpyImg  = coder.decode(self.numpyImg)

    def BCHDecode(self): #TO DO
        logging.debug("Dekodowanie BCH")
        self.BCH_POLYNOMIAL = 8219
        self.BCH_BITS = 17
        self.bch = bchlib.BCH(self.BCH_POLYNOMIAL, self.BCH_BITS)
        self.numpyFlatImg, self.ecc = self.numpyFlatImg[3:-self.bch.ecc_bytes], self.numpyFlatImg[-self.bch.ecc_bytes:]
        print(self.numpyFlatImg.shape)
        self.ecc= bytearray(self.ecc)
        self.ecc= self.ecc[::8]

        self.bch.decode_inplace(self.numpyFlatImg, self.ecc)
        

    ''' Przywracanie kształtów'''   
    def ReShape(self):
        logging.debug("Przywracanie kształtów przez receiver")
        firstDir= self.numpyFlatImg[0]
        secondDir= self.numpyFlatImg[1]
        thirdDir= self.numpyFlatImg[2]
        size=firstDir*secondDir*thirdDir
        
        self.numpyImg=([self.numpyFlatImg[3:size+3]])
        self.numpyImg=np.array(self.numpyImg)
        self.numpyImg=self.numpyImg.transpose()
        self.numpyImg= np.squeeze(self.numpyImg, axis=1)

    def flatArray(self):
        logging.debug("Prostowanie tablicy receiver")
        firstDir= len(self.numpyImg)
        secondDir= len(self.numpyImg[0]) 
        thirdDir= len(self.numpyImg[0][0])
        self.numpyFlatImg=np.zeros(0)
        self.numpyFlatImg+=firstDir
        self.numpyFlatImg+=secondDir
        self.numpyFlatImg+=thirdDir
        np.concatenate((self.numpyFlatImg, self.numpyImg.flatten()), axis=0)
        self.numpyImg=np.reshape(self.numpyImg, (firstDir, secondDir, thirdDir))

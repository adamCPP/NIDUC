from PIL import Image
import numpy as np
import logging
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename


class Sender:

    
    ''' Inicjalizuje logging w trybie debug'''
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Sender created")
        self.img = None
        self.numpyImg = None


    '''Laduje orazek z folderu  resources'''
    def loadPicture(self):
        logging.debug("Your working directory is "+os.getcwd())
        os.chdir(r'./resources')
        Tk().withdraw() 
        filename = askopenfilename() 
        logging.debug("You choosed  "+filename)

        self.img = Image.open(filename)
        self.img.load()

    '''Konwertuje objekt Image na tablicę numpy'''
    def convertImgToNumpyArray(self):
        logging.debug("Konwersja obrazka do numpy array")
        self.numpyImg = np.asarray( self.img, dtype="int32" )

    '''Pokazuje obraz jaki został wczytany tzn przed zakłuceniami wprowadzonymi przez kanał transmisji'''
    def show(self):
        logging.debug("Wysylanie obrazka")
        self.img.show() 


    def send(self):
        logging.debug("Wysylanie obrazka")
        return self.numpyImg()

        

# to nizej to sprawdenie  czy wszystko działa
s = Sender()
s.loadPicture()
s.convertImgToNumpyArray()
s.show()
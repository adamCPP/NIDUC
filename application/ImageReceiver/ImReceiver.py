import logging
from PIL import Image
import numpy as np
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename



class Receiver:

    
    ''' uruchamia logi'''
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Receiver created")
        self.img = None
        self.numpyImg = None

    '''zapisuje otrzymany obraz w postaci numpy array'''
    def receive(self,imageAsNumpyArray):
        logging.debug("Otrzmano obraz w Receiverze")
        self.numpyImg = imageAsNumpyArray


    ''' koweruje numpy array do typu Image zeby mozna bylo wyswietlac'''
    def convertNpyArrayToImage(self):
        logging.debug("Konwersja npyArray do Image w Receiverze")
        self.img = Image.fromarray(self.numpyImg)

    '''pokazuje obraz (nalezy go wczesniej skonwertowac metodą convertNpyArrayToImage)'''
    def show(self):
        logging.debug("Wyświetlenie obrazu w receiverze")
        self.img.show()


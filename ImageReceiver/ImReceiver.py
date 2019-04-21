import logging
from PIL import Image
import numpy as np
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename



class Receiver:

    

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Receiver created")
        self.img = None
        self.numpyImg = None

    def receive(self,imageAsNumpyArray):
        self.numpyImg = imageAsNumpyArray

    def convertNpyArrayToImage(self):
        self.img = Image.fromarray(self.numpyImg)

    def show(self):
        selg.img.show()
r = Receiver()

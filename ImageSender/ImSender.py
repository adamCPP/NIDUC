from PIL import Image
import numpy as np
import logging
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename


class Sender:

    
    
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Receiver created")


    
    def loadPicture(self):
        logging.debug("Your working directory is "+os.getcwd())
        os.chdir(r'./resources')
        Tk().withdraw() 
        filename = askopenfilename() 
        logging.debug("You choosed  "+filename)

        img = Image.open(filename)
        img.load()
        data = np.asarray( img, dtype="int32" )
        img.show()

        


s = Sender()
s.loadPicture()
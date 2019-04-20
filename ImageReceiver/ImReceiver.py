from PIL import Image
import numpy as np
import logging
import os
#from Tkinter import Tk
#from tkinter.filedialog import askopenfilename


class Receiver:

    

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Receiver created")


    
    def loadPicture(self):
        logging.debug("Your working directory is "+os.getcwd())
        '''
        Tk().withdraw() 
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        print(filename)
        '''


s = Receiver()
s.loadPicture()
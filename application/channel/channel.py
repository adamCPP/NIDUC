'''Tutaj sender bedzie przekazywal obrazy. Nastepnie beda wykonywane na nich algorytmy a nastepnie wynik zostanie przekazany do receivera'''
import logging
import numpy as np


class Channel:

    '''Inicjaliuje debug'''
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Channel created")
        self.numpyImg = None
        self.noisyImage = None


    ''' Przekazuje obraz  receivera'''
    def takeImage(self):
        logging.debug("Przekazanie obrazka przez channel")
        return self.noisyImage

    ''' Pobiera obraz z sendera'''
    def receiveImage(self,npyImage):
        logging.debug("Odebranie obrazka przez channel")
        self.numpyImg=npyImage


    '''Dodaje załucenia do obrazu który znajduje się w kanale'''
    def addNoise(self):
        logging.debug("Dudawanie zakłuceń")
        row,col,ch= self.numpyImg.shape
        mean = 0.0
        var = 0.9
        sigma = var**0.5
        gauss = np.array(self.numpyImg.shape)
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        noisy = self.numpyImg + gauss
        self.noisyImage =  noisy.astype('uint8')
    


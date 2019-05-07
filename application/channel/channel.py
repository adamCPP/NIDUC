'''Tutaj sender bedzie przekazywal obrazy. Nastepnie beda wykonywane na nich algorytmy a nastepnie wynik zostanie przekazany do receivera'''
import logging
import numpy as np
from PIL import Image


class Channel:

    '''Inicjaliuje debug'''
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Channel created")
        self.numpyImg = None
        self.numpyFlatImg = None
        self.noisyImage = None


    ''' Przekazuje obraz  receivera'''
    def takeImage(self):
        logging.debug("Przekazanie obrazka przez channel")
        return self.noisyImage
        #return  self.numpyFlatImg

    ''' Pobiera obraz z sendera'''
    def receiveImage(self,npyFlatImage):
        logging.debug("Odebranie obrazka przez channel")
        self.numpyFlatImg=npyFlatImage
     
    ''' Przywracanie kształtów'''   
    def ReShape(self):
        logging.debug("Przywracanie kształtów przez channel")
        firstDir= self.numpyFlatImg[0]
        secondDir= self.numpyFlatImg[1]
        thirdDir= self.numpyFlatImg[2]
        size=firstDir*secondDir*thirdDir
        
        self.numpyImg=([self.numpyFlatImg[3:size+3]])
        self.contrSum=([self.numpyFlatImg[size+3:]])
        self.numpyImg=np.array(self.numpyImg)
        self.numpyImg=self.numpyImg.transpose()
        self.numpyImg= np.squeeze(self.numpyImg, axis=1)
        self.numpyImg=np.reshape(self.numpyImg, (firstDir, secondDir, thirdDir))

    '''Dodaje załócenia do obrazu który znajduje się w kanale'''
    def addNoise(self):
        logging.debug("Dudawanie zakłóceń")
        row,col,ch= self.numpyImg.shape
        mean = 0.0
        var = 0.9
        sigma = var**0.5
        gauss = np.array(self.numpyImg.shape)
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        noisy = self.numpyImg + gauss
        self.noisyImage =  noisy.astype('uint8')

    def show(self):
        logging.debug("Konwersja zaszlumionego obrazu do typu Image")
        image = Image.fromarray(self.noisyImage)
        logging.debug("Wyswietlenie obrazu w channelu")
        image.show()

    def flatArray(self):
        logging.debug("Prostowanie tablicy chanel")
        firstDir= len(self.noisyImage)
        secondDir= len(self.noisyImage[0]) 
        thirdDir= len(self.noisyImage[0][0])
        self.numpyFlatImg=np.array([firstDir, secondDir, thirdDir])
        self.noisyImage= np.concatenate((self.noisyImage, self.noisyImage.flatten()), axis=None)
        self.noisyImage= np.concatenate((self.noisyImage, self.contrSum), axis=None)
    


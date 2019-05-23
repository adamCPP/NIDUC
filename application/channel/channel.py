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
        logging.debug("Channel: Przekazanie obrazka")
        return self.noisyImage
        #return  self.numpyFlatImg

    ''' Pobiera obraz z sendera'''
    def receiveImage(self,npyFlatImage):
        logging.debug("Channel: Odebranie obrazka")
        self.numpyFlatImg=npyFlatImage
     
    ''' Przywracanie kształtów'''   
    def ReShape(self):
        logging.debug("Channel: Przywracanie kształtów")
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
        logging.debug("Channel: Dodawanie zakłóceń")
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
        logging.debug("Channel: Konwersja zaszlumionego obrazu do typu Image")
        image = Image.fromarray(self.noisyImage)
        logging.debug("Channel: Wyswietlenie obrazu")
        image.show()

    def flatArray(self):
        logging.debug("Channel: Prostowanie tablicy ")
        firstDir= len(self.noisyImage)
        secondDir= len(self.noisyImage[0]) 
        thirdDir= len(self.noisyImage[0][0])
        self.numpyFlatImg=np.array([firstDir, secondDir, thirdDir])
        self.noisyImage= np.concatenate((self.noisyImage, self.noisyImage.flatten()), axis=None)
        self.noisyImage= np.concatenate((self.noisyImage, self.contrSum), axis=None)
    


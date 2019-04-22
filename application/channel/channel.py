'''Tutaj sender bedzie przekazywal obrazy. Nastepnie beda wykonywane na nich algorytmy a nastepnie wynik zostanie przekazany do receivera'''
import logging


class Channel:

    '''Inicjaliuje debug'''
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Channel created")
        self.numpyImg = None


    ''' Pobiera obraz z sendera'''
    def takeImage(self):
        logging.debug("Przekazanie obrazka przez channel")
        return self.numpyImg

    ''' Przekazuje obraz de receivera'''
    def receiveImage(self,npyImage):
        logging.debug("Odebranie obrazka przez channel")
        self.numpyImg=npyImage


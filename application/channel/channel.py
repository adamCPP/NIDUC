"""Tutaj sender bedzie przekazywal obrazy. Nastepnie beda wykonywane na nich algorytmy a nastepnie wynik zostanie przekazany do receivera"""
import logging
import numpy as np
from PIL import Image


class Channel:

    """Inicjaliuje debug"""
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Channel created")
        self.numpy_img = None
        self.numpy_flat_img = None
        self.noisy_image = None

        self.numpyImg = None
        self.BCHImage = None
        self.noisyImage = None
        self.BCHImgCopy = None
        self.firstDir=None
        self.secondDir=None
        self.thirdDir=None
        self.size=None

    """Przekazuje obraz do receivera"""
    def take_image(self):
        logging.debug("Channel: Przekazanie obrazka")
        return self.noisy_image
        #return  self.numpyFlatImg

    """Pobiera obraz z sendera"""
    def receive_image(self, npyFlatImage):
        logging.debug("Channel: Odebranie obrazka")
        self.numpy_flat_img = npyFlatImage
     
    """Przywracanie kształtów"""
    def reshape(self):
        logging.debug("Channel: Przywracanie kształtów")
        first_dim = self.numpy_flat_img[0]
        print(f"first dim: {first_dim}")
        second_dim = self.numpy_flat_img[1]
        print(f"sec dim: {second_dim}")
        third_dim = self.numpy_flat_img[2]
        print(f"third dim: {third_dim}")
        size = first_dim * second_dim * third_dim
        
        self.numpy_img = ([self.numpy_flat_img[3:size + 3]])
        self.contr_sum = ([self.numpy_flat_img[size + 3:]])
        self.numpy_img = np.array(self.numpy_img)
        self.numpy_img = self.numpy_img.transpose()
        self.numpy_img = np.squeeze(self.numpy_img, axis=1)
        self.numpy_img = np.reshape(self.numpy_img, (first_dim, second_dim, third_dim))

    """Dodaje załócenia do obrazu który znajduje się w kanale"""
    def add_noise1(self):
        logging.debug("Channel: Dodawanie zakłóceń")
        row, col, ch = self.numpy_img.shape
        mean = 0.0
        var = 0.9
        sigma = var ** 0.5
        gauss = np.array(self.numpy_img.shape)
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = self.numpy_img + gauss
        self.noisy_image = noisy.astype('uint8')

    def add_noise2(self):
        logging.debug("Channel: Dodawanie zakłóceń do salomona")
        mean = 0.0
        var = 0.9
        sigma = var**0.5
        gauss = np.array(self.numpy_flat_img.shape)
        gauss = np.random.normal(mean, sigma, self.numpy_flat_img.shape)
        print(gauss)
        print(self.numpy_flat_img)
        iter = 0
        for val in self.numpy_flat_img:
            if gauss[iter] > 0.95 and val.isdigit():
                val = 'a'
            iter = iter + 1
        self.noisy_image = self.numpy_flat_img

    """Przyjmuje numpy array i zwraca zaszumioną kopię tych samych wymiarów"""
    @staticmethod
    def add_noise(data, mean=0.0, var=None, sigma=None):
        assert not (var and sigma)
        if var:
            sigma = var ** 0.5
        elif not sigma:
            sigma = 0.23

        unpacked_data = np.unpackbits(data)
        noise = np.random.normal(mean, sigma, unpacked_data.shape)
        noised_unpacked_data = unpacked_data + noise
        rounded_noised_unpacked_data = np.array([0] * len(unpacked_data))
        for i, val in enumerate(noised_unpacked_data):
            if val < 0.5:
                rounded_noised_unpacked_data[i] = 0
            else:
                rounded_noised_unpacked_data[i] = 1
        packed_noised = np.packbits(rounded_noised_unpacked_data).reshape(data.shape)
        return packed_noised

    def add_noise_to_numpy_flat_img(self):
        logging.debug("Dodawanie zakłóceń do numpy_flat_img")
        self.noisy_image = self.add_noise(self.numpy_flat_img)
        return None
        mean = 0.0
        var = 0.05
        sigma = var ** 0.5
        numpy_array_unpacked = np.unpackbits(self.numpy_flat_img)
        gauss = np.random.normal(mean, sigma, numpy_array_unpacked.shape)
        noisy_unpacked = numpy_array_unpacked + gauss
        for i, val in enumerate(noisy_unpacked):
            numpy_array_unpacked[i] = 0 if val < 0.5 else 1
        self.noisy_image = np.reshape(np.packbits(numpy_array_unpacked), self.numpy_flat_img.shape)
        self.noisy_image = self.noisy_image.astype('uint8')

    def add_noise3(self):
        logging.debug("Channel: Dodawanie zakłóceń do potrajania bitów")
        mean = 0.0
        var = 0.9
        sigma = var ** 0.5
        gauss = np.array(self.numpy_flat_img.shape)
        gauss = np.random.normal(mean, sigma, self.numpy_flat_img.shape)
        print(gauss)
        print(self.numpy_flat_img)
        iter = 0
        for val in self.numpy_flat_img:
            if gauss[iter] > 0.9:
                self.numpy_flat_img[iter] = 0
            iter = iter + 1
        self.noisy_image = self.numpy_flat_img
        print(self.numpy_flat_img)

    def show(self):
        logging.debug("Channel: Konwersja zaszlumionego obrazu do typu Image")
        image = Image.fromarray(self.noisy_image)
        logging.debug("Channel: Wyswietlenie obrazu")
        image.show()

    def BCHshow(self):
        logging.debug("Channel: Konwersja zaszlumionego obrazu do typu Image")
        image = Image.fromarray(self.noisyImage)
        logging.debug("Channel: Wyswietlenie obrazu")
        image.show()

    def flat_array(self):
        logging.debug("Channel: Prostowanie tablicy ")
        first_dim = len(self.noisy_image)
        second_dim = len(self.noisy_image[0])
        third_dim = len(self.noisy_image[0][0])
        self.numpy_flat_img = np.array([first_dim, second_dim, third_dim])
        self.noisy_image = np.concatenate((self.noisy_image, self.noisy_image.flatten()), axis=None)
        self.noisy_image = np.concatenate((self.noisy_image, self.contr_sum), axis=None)

    def BCHreceiveImage(self, Encoded, sizeX, sizeY, sizeZ):
        logging.debug("CHANEL		Odebranie obrazka przez channel")
        self.BCHImage=Encoded
        self.BCHImgCopy=Encoded
        self.firstDir=sizeX
        self.secondDir=sizeY
        self.thirdDir=sizeZ
        self.size=self.firstDir*self.secondDir*self.thirdDir

    def BCHdePacketize(self):
        logging.debug("CHANEL		BCH depacketize")
        depacket=bytearray()
        for x in range(0, int(len(self.BCHImage)/712)):
                depacket=depacket+self.BCHImage[712*x:712*x+512]
        self.BCHImage=depacket

    def BCHtoNumArray(self):
        logging.debug("CHANEL		BCHImg to numpy array")
        self.numpyImg= np.array(self.BCHImage[:self.size])
        self.BCHImage= np.frombuffer(self.numpyImg, dtype=np.uint8)
     
    def BCHReShape(self):
        logging.debug("CHANEL		Przywracanie kształtów przez channel")
        self.numpyImg=np.array([1])
        self.numpyImg=np.reshape(self.BCHImage.transpose(), (self.firstDir, self.secondDir, self.thirdDir))


    def BCHflatArray(self):
        logging.debug("CHANEL		Prostowanie tablicy")
        self.BCHImage= np.array([1])
        self.BCHImage= np.concatenate((self.BCHImage, self.noisyImage.flatten()), axis= None)

    def BCHtoByteArray(self):
        logging.debug("CHANEL		zamiana obrazka na ByteArray")
        repacket=bytearray()
        self.BCHImage = bytearray(self.BCHImage)[8::8]
        mod_size= self.size % 512
        self.BCHImage= self.BCHImage+ bytearray(512-mod_size)
        for x in range(0, int(len(self.BCHImage)/512)):
                packet=self.BCHImage[x*512:(x+1)*512]+self.BCHImgCopy[(x)*712+512:(x+1)*712]
                repacket= repacket+packet
        self.BCHImage=repacket

    def BCHsend(self):
        logging.debug("CHANEL		Przekazanie bytearray przez channel")
        return  self.BCHImage

    def BCHsendX(self):
        logging.debug("CHANEL		Wymiar 1")
        return self.firstDir

    def BCHsendY(self):
        logging.debug("CHANEL		Wymiar 2")
        return self.secondDir

    def BCHsendZ(self):
        logging.debug("CHANEL		Wymiar 3")
        return self.thirdDir

    def addNoise(self):
        logging.debug("CHANEL		Dudawanie zakłóceń")
        mean = 0.0
        var = 0.6
        sigma = var**0.5
        gauss = np.array(self.numpyImg.shape)
        gauss = np.random.normal(mean,sigma,(self.firstDir,self.secondDir,self.thirdDir))
        gauss = gauss.reshape(self.firstDir,self.secondDir,self.thirdDir)
        noisy = self.numpyImg + gauss
        self.noisyImage = noisy.astype('uint8')

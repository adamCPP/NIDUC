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
    def add_noise(self):
        logging.debug("Channel: Dodawanie zakłóceń")
        row, col, ch = self.numpy_img.shape
        mean = 0.0
        var = 0.9
        sigma = var**0.5
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

    def add_noise_to_numpy_flat_img(self):
        logging.debug("Dodawanie zakłóceń do numpy_flat_img")
        mean = 0.0
        var = 0.9
        sigma = var ** 0.5
        gauss = np.array(self.numpy_flat_img.shape)
        gauss = np.random.normal(mean, sigma, self.numpy_flat_img.shape)
        gauss = gauss.reshape(self.numpy_flat_img.shape)
        self.noisy_image = self.numpy_flat_img + gauss
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
                self.numpy_flat_img[iter]=0
            iter = iter + 1
        self.noisy_image = self.numpy_flat_img

        print(self.numpy_flat_img)

    def show(self):
        logging.debug("Channel: Konwersja zaszlumionego obrazu do typu Image")
        image = Image.fromarray(self.noisy_image)
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
    


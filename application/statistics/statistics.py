from PIL import Image
from PIL import ImageChops
import logging
import numpy as np


class Statistics:

    """Inicjalizuje zmienne domyślnymi wartościami"""
    def __init__(self, original_img, noisy_img, noise_type, primary_ber, coding):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Stworzenie obiektu Statistics")

        self.original_img = original_img
        self.noisy_img = noisy_img
        self.noise_type = noise_type
        self.coding = coding
        self.primary_ber = primary_ber

        if original_img and noisy_img:
            self.img_format = original_img.format
            self.diff_img = ImageChops.difference(original_img, noisy_img)
            self.img_error_bits, self.img_size = self.bits_difference()
            self.ber = self.img_error_bits / self.img_size
            logging.info(f"Statistics: BER = {self.ber}")

    """Używane przez pickle do składowania obiektu bez obrazów"""
    def __getstate__(self):
        state = self.__dict__.copy()
        del state["original_img"]
        del state["noisy_img"]
        del state["diff_img"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.original_img = None
        self.noisy_img = None
        self.diff_img = None
        self.baz = 0

    """Tworzy obraz pokazujący zmienione piksele"""
    @staticmethod
    def difference_img(img1, img2):
        logging.debug("Statistics: Difference image")
        diff_img = ImageChops.difference(img1, img2)
        diff_img.show()

    """Wyznacza liczbę błędów i bitów"""
    def bits_difference(self):
        original_unpacked = np.unpackbits(np.array(self.original_img))
        noisy_unpacked = np.unpackbits(np.array(self.noisy_img))
        errors_count = 0
        img_size = len(original_unpacked)
        for i in range(img_size):
            if original_unpacked[i] != noisy_unpacked[i]:
                errors_count += 1
        return errors_count, img_size

from PIL import Image
from PIL import ImageChops
import logging


class Statistics:

    """Inicjalizuje zmienne domyślnymi wartościami"""
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Stworzenie obiektu Statistics")
        original = None
        noisy_img = None

    """Tworzy obraz pokazujący zmienione piksele"""
    @staticmethod
    def difference_img(img1, img2):
        logging.debug("Statistics: Difference image")
        diff_img = ImageChops.difference(img1, img2)
        diff_img.show()
        pass

    """Zwraca wartość zmienionych bitów w procentach"""
    def difference_percent(self):
        pass

    """Zwraca wartość absolutną zmienionych pikseli"""
    def difference_total(self):
        pass

    """Zapisuje statystyki w pliku"""
    def save(self):
        pass

from PIL import Image
import numpy as np
import logging
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import unireedsolomon as rs
import bchlib
import random
import math
import textwrap


class Sender:

    """Inicjalizuje logging w trybie debug"""
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Sender created")
        self.img = None
        self.numpy_img = None
        self.numpy_flat_img = None
        self.bytearray_img = None

        self.bch_numpy_img = None
        self.bch_numpy_flat_img = None
        self.bch_bch_size = None
        self.bch_packet = []
        self.bch_encoded = bytearray()

        self.bch_size = None
        self.first_dir = None
        self.second_dir = None
        self.third_dir = None

    """Laduje orazek z folderu  resources"""
    def load_picture(self):
        logging.debug("Sender: Your working directory is " + os.getcwd())
        os.chdir(r'./application/resources')
        Tk().withdraw() 
        filename = askopenfilename() 
        logging.debug("Sender: You choosed  " + filename)

        self.img = Image.open(filename)
        self.img.load()
        os.chdir(r'./../..')

    """Konwertuje objekt Image na tablicę numpy"""
    def converting_to_numpy_array(self):
        logging.debug("Sender: Konwersja obrazka do numpy array")
        self.numpy_img = np.array(self.img)

    """Konwertuje obiekt Image do bytearray"""
    def convert_img_to_bytearray(self):
        logging.debug("Sender: Konwersja obrazu do bytearray")
        self.bytearray_img = bytearray(self.img.tobytes())

    """Pokazuje obraz jaki został wczytany tzn przed zakłóceniami wprowadzonymi przez kanał transmisji"""
    def show(self):
        logging.debug("Sender: Wyswietlenie obrazka")
        self.img.show(title='Oryginał')

    def send(self):
        logging.debug("Sender: Wysylanie obrazka")
        return self.numpy_flat_img

    def flat_array(self):
        logging.debug("Sender: Prostowanie tablicy")
        first_dim = len(self.numpy_img)
        second_dim = len(self.numpy_img[0])
        third_dim = len(self.numpy_img[0][0])
        self.numpy_flat_img = np.array([first_dim, second_dim, third_dim])
        self.numpy_flat_img = np.concatenate((self.numpy_flat_img, self.numpy_img.flatten()), axis=None)

    def reed_solomon_encode(self): 

        logging.debug("Sender: Kodowanie reeda solomona")
        #self.numpy_flat_img = np.array(self.numpy_flat_img[0:1000])
        coder = rs.RSCoder(255,223)
        output = []
        logging.debug("Sender: Numpy flat image")
        logging.debug(self.numpy_flat_img)
        logging.debug(self.numpy_flat_img.shape)
    
        print("Dlugosc stringa"+str(len(self.numpy_flat_img)))
        s = ""
        s = s + str(self.numpy_flat_img[0])
        for i in range(1, self.numpy_flat_img.shape[0]):
            s = s + " " + str(self.numpy_flat_img[i])

        self.numpy_flat_img = s

        logging.debug("Sender: Numpy string")
        print(self.numpy_flat_img)
        
        blocks = textwrap.wrap(self.numpy_flat_img,223)
        for block in blocks:
            code = coder.encode(block)
            logging.debug("block")
            logging.debug(block)
            output.append(code)
        self.numpy_flat_img=np.array(output)
        logging.debug("Sender: output shape")
        logging.debug(self.numpy_flat_img.shape)
        logging.debug("Sender: output ")
        logging.debug(self.numpy_flat_img[0])

    def bch_flat_array(self):
        logging.debug("SENDER		Prostowanie tablicy")
        self.bch_size_x= len(self.bch_numpy_img)
        self.bch_size_y= len(self.bch_numpy_img[0]) 
        self.bch_size_z= len(self.bch_numpy_img[0][0])
        self.bch_size=self.bch_size_x* self.bch_size_y* self.bch_size_z
        self.bch_numpy_flat_img= np.array([1])
        self.bch_numpy_flat_img= np.concatenate((self.bch_numpy_flat_img, self.bch_numpy_img.flatten()), axis= None)

    def bch_to_byte_array(self):
        logging.debug("SENDER		zamiana obrazka na ByteArray")
        self.bch_numpy_flat_img = bytearray(self.bch_numpy_flat_img)[8::8]

    def bch_boundling(self):
        logging.debug("SENDER		Pakietyzacja BCH")
        mod_bch_size=self.bch_size % 512
        self.bch_numpy_flat_img = self.bch_numpy_flat_img + bytearray(512-mod_bch_size)
        for x in range(0, int(len(self.bch_numpy_flat_img)/512)):
                self.bch_packet.append(self.bch_numpy_flat_img[x*512:(x+1)*512])

    def bch_encode(self):
        logging.debug("SENDER		Kodowanie BCH")
        BCH_POLYNOMIAL = 8219
        BCH_BITS = 123
        bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)
        for x in range(0, len(self.bch_packet)):
                ecc = bch.encode(self.bch_packet[x])
                self.bch_packet[x]=self.bch_packet[x]+ecc
                self.bch_encoded= self.bch_encoded+(self.bch_packet[x])

    def bch_send(self):
        logging.debug("SENDER		Wysylanie bytearray")
        return self.bch_encoded

    def bch_send_x(self):
        logging.debug("SENDER		Wymiar 1")
        return self.bch_size_x

    def bch_send_y(self):
        logging.debug("SENDER		Wymiar 2")
        return self.bch_size_y

    def bch_send_z(self):
        logging.debug("SENDER		Wymiar 3")
        return self.bch_size_z        

    def bch_load_picture(self):
        logging.debug("Your working directory is "+os.getcwd())
        os.chdir(r'./application/resources')
        Tk().withdraw() 
        filename = askopenfilename() 
        logging.debug("You choosed  "+filename)
        self.img = Image.open(filename)
        self.img.load()

    def bch_convert_img_to_numpy_array(self):
        logging.debug("SENDER		Konwersja obrazka do numpy array")
        self.bch_numpy_img = np.array(self.img)

    def triple_encode(self): # kodowanie  tylko 10 pierwszych elementow
        logging.debug("Sender: potrajanie bitów")

        logging.debug("Sender: Oryginalna tablica")
        logging.debug(self.numpy_flat_img[0:10])
        output = []

        for i in range(0,len(self.numpy_flat_img[0:10])):
            for j in range(0,3):
                output.append(self.numpy_flat_img[i])

        logging.debug("Sender: Potrojona tablica")
        print(output)

        self.numpy_flat_img  = np.array(output)

        print("Len:")
        print(len(self.numpy_flat_img))


# to nizej to sprawdenie  czy wszystko działa
'''
s = Sender()
s.loadPicture()
s.convertImgToNumpyArray()
s.show()
'''

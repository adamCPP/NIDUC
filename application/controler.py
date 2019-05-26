"""Glowna aplikacja"""


from image_receiver.im_receiver  import Receiver
from image_sender.im_sender import Sender
from channel.channel import Channel
import logging
import tkinter  as tk
from tkinter.filedialog import askopenfilename

class Controler:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Controler created")
        self.main()

    def exit(self):
        quit()

    def main(self):
        logging.debug("Main")
        HEIGH = 150
        WIDTH = 200

        root = tk.Tk()
        root.title("Forward Error Correction")

        canvas = tk.Canvas(root,heigh=HEIGH,width=WIDTH)
        canvas.pack()

        frame = tk.Frame(root,bg="#808080")
        frame.place(relwidth=1,relheight=1)

        button_sal = tk.Button(frame,text="Reed Solomon",command=self.reed_solomon)
        button_sal.pack()
        button_triple = tk.Button(frame,text="Potrajanie bitów",command=self.triple)
        button_triple.pack()
        button_ham = tk.Button(frame,text="Hamming")
        button_ham.pack()
        button_bch = tk.Button(frame,text="BCH",command=self.bch)
        button_bch.pack()
        button_exit = tk.Button(frame,text="Wyjście",command=self.exit)
        button_exit.pack()

        root.mainloop()

    def hamming(self):
        logging.debug("Hamming")

    def reed_solomon(self):
        logging.debug("Reed Solomon")


        r = Receiver()
        s = Sender()
        c = Channel()

        #zaladowanie obrazka, konwersja do numpyArray i wyświetlenie obrazu przed wysłaniem
        s.load_picture()
        s.converting_to_numpy_array()
        s.show()

        #Tworzenie tablicy 1D
        s.flat_array()

        #kodowanie reeda solomona
        s.reed_solomon_encode()


        # wysłanie obrazka do kanał
        c.receive_image(s.send())

        #zauszumienie
        c.add_noise2()


        #oderanie obrazka z kanału
        r.receive_img_as_np_array(c.take_image())

        r.reed_solomon_decode()

        r.reshape()
        r.convert_numpy_array_to_image()
        r.show()



    def bch(self):
        logging.debug("BCH")


        # tworzenie  glównych komponentów
        r = Receiver()
        s = Sender()
        c = Channel()

        # zaladowanie obrazka, konwersja do numpyArray i wyświetlenie obrazu przed wysłaniem
        s.load_picture()
        s.converting_to_numpy_array()
        s.show()

        # Tworzenie tablicy 1D
        s.flat_array()

        # kodowanie reeda solomona
        s.reed_solomon_encode()

        # kodowanie BCH
        # s.BCHEncode()

        # wysłanie obrazka do kanał
        c.receive_image(s.send())

        # Przywracanie wymiarów
        c.reshape()

        # zauszumienie
        c.add_noise()

        # wyświetlenie zaszuumionego obazu
        c.show()

        # Tworzenie tablicy 1D
        c.flat_array()

        # oderanie obrazka z kanału
        r.receive(c.take_image())

        # prostowanie tablicy
        # r.BCHDecode()

        r.reshape()
        # konwersja npyArray to obrazu i wyświetlenie go

        r.convert_numpy_array_to_image()
        r.show()


    def triple(self):
        logging.debug("Triple")

        r = Receiver()
        s = Sender()
        c = Channel()

        s.load_picture()
        s.converting_to_numpy_array()
        s.show()

        s.flat_array()

        s.triple_encode()

        c.receive_image(s.send())

        c.add_noise3()

        r.receive_img_as_np_array(c.take_image())

        r.triple_decode()

        r.reshape()
        r.convert_numpy_array_to_image()
        r.show()




con = Controler()

#con.reed_solomon()
con.triple()



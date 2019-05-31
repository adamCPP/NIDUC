"""Glowna aplikacja"""


from application.image_receiver.im_receiver  import Receiver
from application.image_sender.im_sender import Sender
from application.channel.channel import Channel
from application.hamming.hamming import Hamming
import logging
import tkinter as tk
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
        HEIGH = 180
        WIDTH = 200

        root = tk.Tk()
        root.title("Forward Error Correction")

        canvas = tk.Canvas(root, heigh=HEIGH, width=WIDTH)
        canvas.pack()

        frame = tk.Frame(root, bg="#808080")
        frame.place(relwidth=1, relheight=1)

        button_non = tk.Button(frame, text="Bez kodowania", command=self.without_coding)
        button_non.pack()
        button_sal = tk.Button(frame, text="Reed Solomon", command=self.reed_solomon)
        button_sal.pack()
        button_triple = tk.Button(frame, text="Potrajanie bitów", command=self.triple)
        button_triple.pack()
        button_ham = tk.Button(frame, text="Hamming", command=self.hamming)
        button_ham.pack()
        button_bch = tk.Button(frame, text="BCH", command=self.bch)
        button_bch.pack()
        button_exit = tk.Button(frame, text="Wyjście", command=self.exit)
        button_exit.pack()

        root.mainloop()

    def without_coding(self):
        logging.debug("Bez kodowania")
        sender = Sender()
        simple_channel = Channel()
        simple_receiver = Receiver()

        sender.load_picture()
        sender.converting_to_numpy_array()
        sender.show()

        simple_channel.receive_image(sender.numpy_img)
        simple_channel.add_noise_to_numpy_flat_img()

        simple_receiver.receive_img_as_np_array(simple_channel.take_image())
        simple_receiver.reshape(sender.numpy_img.shape)
        simple_receiver.convert_numpy_array_to_image()
        simple_receiver.show()

    def hamming(self):
        logging.debug("Hamming")
        hamming = Hamming()
        sender = Sender()
        channel = Channel()
        receiver = Receiver()

        sender.load_picture()
        sender.converting_to_numpy_array()
        sender.show()

        print(sender.numpy_img.shape)

        encoded = hamming.encode(sender.numpy_img)
        channel.receive_image(encoded)
        channel.add_noise_to_numpy_flat_img()

        receiver.receive_img_as_np_array(channel.take_image())
        decoded = hamming.decode(receiver.numpy_flat_img)
        receiver.numpy_flat_img = decoded

        receiver.reshape(sender.numpy_img.shape)
        receiver.convert_numpy_array_to_image()
        receiver.show()

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

        #zaladowanie obrazka, konwersja do numpyArray i wyświetlenie obrazu przed wysłaniem
        s.loadPicture()
        s.convertImgToNumpyArray()
        s.show()
        #-------------------------------------------
        #Tworzenie tablicy 1D
        s.BCHflatArray()
        #zmiana formatu
        s.BCHtoByteArray()
        s.BCHPacketize()
        #kodowanie BCH
        s.BCHEncode()
        #-------------------------------------------
        # wysłanie obrazka do kanał
        c.BCHreceiveImage(s.BCHsend(),s.BCHsendX(),s.BCHsendY(),s.BCHsendZ())
        #-------------------------------------------
        c.BCHdePacketize()
        #zmiana formatu
        c.BCHtoNumArray()
        #Przywracanie wymiarów
        c.BCHReShape()
        #zauszumienie
        c.addNoise()
        #wyświetlenie zaszuumionego obazu
        c.BCHshow()
        #Tworzenie tablicy 1D
        c.BCHflatArray()
        #zmiana formatu
        c.BCHtoByteArray()
        #-------------------------------------------
        #oderanie obrazka z kanału
        r.BCHreceive(c.BCHsend(), c.BCHsendX(), c.BCHsendY(), c.BCHsendZ())
        #-------------------------------------------
        r.BCHdePacketize()
        #zmiana formatu
        r.BCHtoNumArray()
        #Przywracanie wymiarów
        r.BCHReShape()
        #-------------------------------------------
        # konwersja npyArray na obraz i wyświetlenie go
        r.convertNpyArrayToImage()
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

# con.reed_solomon()
con.triple()



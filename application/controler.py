"""Glowna aplikacja"""


from image_receiver.im_receiver  import Receiver
from image_sender.im_sender import Sender
from channel.channel import Channel


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

'''
******************
***Reed Solomon***
******************
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




'''

'''
*********
***BCH***
*********


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
>>>>>>> da0be4be2e251844a6843d352d43aa92c0788296

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
'''

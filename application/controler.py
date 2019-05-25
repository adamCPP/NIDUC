"""Glowna aplikacja"""

from application.image_receiver.im_receiver  import Receiver
from application.image_sender.im_sender import Sender
from application.channel.channel import Channel

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

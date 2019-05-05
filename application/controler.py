''' Glowna aplikacja'''

from ImageReceiver.ImReceiver  import Receiver
from ImageSender.ImSender import Sender
from channel.channel import Channel

# tworzenie  glównych komponentów
r = Receiver()
s = Sender()
c = Channel()

#zaladowanie obrazka, konwersja do numpyArray i wyświetlenie obrazu przed wysłaniem
s.loadPicture()
s.convertImgToNumpyArray()
s.show()

#Tworzenie tablicy 1D
s.floatArray()

#kodowanie reeda solomona
s.reedSolomonEncode()

#kodowanie BCH
#s.BCHEncode()

# wysłanie obrazka do kanał
c.receiveImage(s.send())

#Przywracanie wymiarów
c.ReShape()

#zauszumienie
c.addNoise()

#wyświetlenie zaszuumionego obazu
c.show()

#Tworzenie tablicy 1D
c.floatArray()

#oderanie obrazka z kanału
r.receive(c.takeImage())

# konwersja npyArray to obrazu i wyświetlenie go 
r.convertNpyArrayToImage()
r.show()

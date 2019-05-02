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

# wysłanie obrazka do kanał
c.receiveImage(s.send())

#zauszumienie
c.addNoise()

#wyświetlenie zaszuumionego obazu

c.show()

#oderanie obrazka z kanału
r.receive(c.takeImage())

# konwersja npyArray to obrazu i wyświetlenie go 
r.convertNpyArrayToImage()
r.show()

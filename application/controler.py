''' Glowna aplikacja'''

from ImageReceiver.ImReceiver  import Receiver
from ImageSender.ImSender import Sender
from channel.channel import Channel

r = Receiver()
s = Sender()
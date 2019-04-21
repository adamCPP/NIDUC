

class Receiver:

    

    def __init__(self):
        print("Receiver created")

    def imRead(self,path):

        self.image = Image.open(path)
r = Receiver()
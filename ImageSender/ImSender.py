

class Sender:

    

    def __init__(self):
        print("Sender created")

    def imRead(self,path):

        self.image = Image.open(path)
s = Sender()
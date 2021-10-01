class File:
    def __init__(self):
        self.file=[]
    def ajouter(self, coord):
        self.file.append(coord)
    def sortir(self):
        if(len(self.file)!=0):
            return self.file.pop(0)
        else:
            return -1
    def reset(self):
        self.file=[]
    def estVide(self):
        return self.file==[]
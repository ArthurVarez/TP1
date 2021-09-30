from tkinter import *
from Manoir import *
from Aspirateur import *
class Main:
    def __init__(self):
        taille = 5
        self.fenetre = Tk()
        self.canvas = Canvas(self.fenetre, width=taille*70, height=taille*70)
        self.manoir = Manoir(taille, self.canvas)

        self.manoir.ajouterPoussiere()
        self.manoir.ajouterPoussiere()
        self.manoir.ajouterPoussiere()

        self.manoir.ajouterBijou()
        self.manoir.ajouterBijou()
        self.manoir.ajouterBijou()
        self.aspirateur = Aspirateur(self.manoir, self.canvas)
        self.bouton = Button(text ="Start")

    def start(self):
        self.manoir.start()
        self.aspirateur.start()
        self.canvas.pack()
        self.bouton.pack()
        self.fenetre.mainloop()

build = Main()
build.start()


from tkinter import *
from Manoir import *
from Aspirateur import *
class Main:
    def __init__(self):
        taille = 5
        self.fenetre = Tk()
        self.fenetre.title("Nettoyage de manoir")
        self.modeBoutonsLabelFrame = LabelFrame(self.fenetre, text = "Modes de recherche")
        self.manoirLabelFrame = LabelFrame(self.modeBoutonsLabelFrame, text="Manoir")

        self.canvas = Canvas(self.manoirLabelFrame, width=taille*70, height=taille*70)
        self.manoir = Manoir(taille, self.canvas)

        self.manoir.ajouterPoussiere()
        self.manoir.ajouterPoussiere()
        self.manoir.ajouterPoussiere()

        self.manoir.ajouterBijou()
        self.manoir.ajouterBijou()
        self.manoir.ajouterBijou()

        self.aspirateur = Aspirateur(self.manoir, self.canvas)
        self.modeNonInforme = Radiobutton(self.modeBoutonsLabelFrame, text="Non informé", variable=self.aspirateur.modeRecherche, value="1")
        self.modeInforme = Radiobutton(self.modeBoutonsLabelFrame, text="Informé", variable=self.aspirateur.modeRecherche, value="0")
        self.bouton = Button(text ="Start")
        self.perfLabelFrame = LabelFrame(self.manoirLabelFrame, text ="Mesure de performance")
        self.consoLabel = Label(self.perfLabelFrame, textvariable=self.aspirateur.consoStringVar)
        self.scoreLabel = Label(self.perfLabelFrame, textvariable = self.aspirateur.scoreStringVar)

    def start(self):
        self.manoir.start()
        self.aspirateur.start()
        self.modeBoutonsLabelFrame.pack()
        self.modeInforme.pack()
        self.modeNonInforme.pack()
        self.manoirLabelFrame.pack()

        self.canvas.pack()
        self.perfLabelFrame.pack(fill='x')
        self.consoLabel.pack()
        self.scoreLabel.pack()
       # self.bouton.pack()
        self.fenetre.mainloop()

build = Main()
build.start()


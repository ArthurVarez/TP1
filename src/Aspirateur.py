# -*- coding: utf-8 -*-
from Capteur import *
from tkinter import *
from Effecteur import *
from File import *
import math
import time
import threading
class Aspirateur(threading.Thread):
    def __init__(self,manoir, canvas):

        threading.Thread.__init__(self)
        self.aspi_icon = PhotoImage(file='../img/icons/roomba_f.png')
        self.canvas = canvas
        self.aspirateurDejaDessinee = 0

        #### Environnemment
        self.manoir = manoir

        #### Mesure de performance
        self.consoStringVar = StringVar()
        self.scoreStringVar = StringVar()
        self.consommation=0
        self.score=0
        self.scoreStringVar.set("Score : "+str(self.score))
        self.consoStringVar.set("Consommation : "+str(self.consommation))

        #### Etats
        self.position=[0,0]
        self.positionsPoussieres=[]
        self.positionsBijoux=[]

        #### Mouvement désiré
        self.mouvement=[0,0]

        #### Effecteur et Capteur
        self.capteur = Capteur()
        self.effecteur = Effecteur()

        #### Mode de recherche
        self.modeRecherche = StringVar()
        self.modeRecherche.set("0")

        #### Mode non informé
        self.file = File()
        self.NoeudsVisites=[0 for i in range(self.manoir.taille**2)]
        self.NoeudsPrecedents=[None for i in range(self.manoir.taille**2)]
        self.cheminASuivre=[]

    def run(self):
        self.afficherAspirateur()
        while(1):
            if(self.modeRecherche.get()=="0"):
                self.capteur.capterEnvironnemment(self,self.manoir)
                if(self.manoirPropre()!=True):
                    self.mouvement = self.prendreDecision()
                    print("Le manoir est encore sale, je vais voir ce que je peux faire")
                else:
                    print("Le manoir est propre, je me mets en pause")
                time.sleep(1)
            elif(self.modeRecherche.get()=="1"):
                self.capteur.capterEnvironnemment(self,self.manoir)
                self.prendreDecisionNonInforme()
                if(self.manoirPropre()!=True):
                    if(self.cheminASuivre==[]):
                        print("Rien à faire, je reste sur place")
                    else:
                        self.calculerMouvement(self.cheminASuivre[0])
                        self.effecteur.effectuerMouvement(self,self.mouvement)
                        self.updateConso()
                        self.updateAspirateur(self.mouvement)
                else:
                    print("Le manoir est propre, je me mets en pause")
                time.sleep(1)


    def prendreDecision(self):
        if(self.position in self.positionsBijoux):
            self.ramasserBijou()
            print("Il y a un bijou où je suis, je le ramasse")
        elif(self.position in self.positionsPoussieres):
            self.aspirer()
            print("Il y a de la poussière où je suis, j'aspire'")
        else:
            print("Il n'y a rien où je suis, je dois me déplacer")
            self.prendreDecisionMouvement()
            self.effecteur.effectuerMouvement(self, self.mouvement)
            self.updateAspirateur(self.mouvement)
            self.updateConso()

    def prendreDecisionMouvement(self):
        heuristique = math.inf
        newHeuristique = 0
        coordPlusProcheAvecPoussiere = self.definirObjectif()
        coordVoisins = self.connaitrePlusProchesVoisins()
        coordVersQuiBouger = self.position
        for coord in coordVoisins:
            newHeuristique = self.calculerDistanceEuclidienne(coord, coordPlusProcheAvecPoussiere[0])
            if(newHeuristique<heuristique):
                heuristique = newHeuristique
                coordVersQuiBouger = coord
        self.mouvement = [b-a for a,b in zip(self.position,coordVersQuiBouger)]

    def connaitrePlusProchesVoisins(self):
        coordVoisins = []
        taille = self.manoir.taille
        indexCoordMatriceAdjacence = self.position[0]*taille + self.position[1]
        for j in range(taille*taille):
            if(self.manoir.matriceAdjacence[indexCoordMatriceAdjacence][j]==1):
                coordVoisinJ = j%taille
                coordVoisinI = math.floor((j-coordVoisinJ)/taille)
                coordVoisins.append([coordVoisinI,coordVoisinJ])
        return coordVoisins

    def connaitrePlusProchesVoisins1(self, coord):
        coordVoisins = []
        taille = self.manoir.taille
        indexCoordMatriceAdjacence = coord[0]*taille + coord[1]
        for j in range(taille*taille):
            if(self.manoir.matriceAdjacence[indexCoordMatriceAdjacence][j]==1):
                coordVoisinJ = j%taille
                coordVoisinI = math.floor((j-coordVoisinJ)/taille)
                coordVoisins.append([coordVoisinI,coordVoisinJ])
        return coordVoisins


    def definirObjectif(self):
        distanceMin=math.inf
        coordPlusProche=self.position
        newDistanceMin=0
        positionsObjets=self.positionsPoussieres+self.positionsBijoux
        for coord in positionsObjets:
            newDistanceMin=self.calculerDistanceEuclidienne(self.position,coord)
            if(newDistanceMin<distanceMin):
                distanceMin=newDistanceMin
                coordPlusProche=coord
        print("Je veux me déplacer vers "+str(coordPlusProche))
        return [coordPlusProche, distanceMin]

    def calculerDistanceEuclidienne(self, a, b):
        return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

    def manoirPropre(self):
        positionsObjets=self.positionsPoussieres+self.positionsBijoux
        return positionsObjets==[]

    def aspirer(self):
        self.manoir.grille[self.position[0]][self.position[1]][0]=0
        self.updateConso()
        self.updateScore()
        indexPoussiere = self.position[0]*self.manoir.taille+self.position[1]
        self.canvas.delete(self.manoir.dicoPoussiere[indexPoussiere])
        print("J'aspire à la position "+str(self.position))

    def ramasserBijou(self):
        self.manoir.grille[self.position[0]][self.position[1]][1]=0
        self.updateConso()
        self.updateScore()
        indexBijou = self.position[0]*self.manoir.taille+self.position[1]
        print(self.manoir.dicoBijou[indexBijou])
        self.canvas.delete(self.manoir.dicoBijou[indexBijou])
        print("Je ramasse un bijou à la position "+str(self.position))

    def afficherAspirateur(self):
        if(self.aspirateurDejaDessinee==0):
            self.canvasId=self.canvas.create_image(70*self.position[0],70*self.position[1],anchor=NW,image=self.aspi_icon)
            self.aspirateurDejaDessinee=1

    def updateAspirateur(self, mouvement):
            self.canvas.move(self.canvasId, mouvement[0]*70, mouvement[1]*70)

    def updateConso(self):
        self.consommation+=1
        self.consoStringVar.set("Consommatrion : "+str(self.consommation))

    def updateScore(self):
        self.score+=1
        self.scoreStringVar.set("Score : "+str(self.score))
############ ALGO DE LA PARTIE NON INFORMÉE
    def prendreDecisionNonInforme(self):
        if(self.position in self.positionsBijoux):
            self.ramasserBijou()
        elif(self.position in self.positionsPoussieres):
            self.aspirer()
        else:
            self.definirObjectif()
            self.deplacementNonInforme()

    def deplacementNonInforme(self):
        coordVoisins = None
        self.file.reset()
        self.file.ajouter(self.position)
        self.NoeudsVisites=[0 for i in range(self.manoir.taille**2)]
        self.NoeudsPrecedents=[None for i in range(self.manoir.taille**2)]
        self.cheminASuivre=[]
        self.NoeudsVisites[self.calculerIndexCoord(self.position)]=1
        noeud=None
        while(self.file.estVide()!=True):
            noeud=self.file.sortir()
            coordVoisins = self.connaitrePlusProchesVoisins1(noeud)
            for suivant in coordVoisins:
                if(self.NoeudsVisites[self.calculerIndexCoord(suivant)]==0):
                    self.file.ajouter(suivant)
                    self.NoeudsVisites[self.calculerIndexCoord(suivant)]=1
                    self.NoeudsPrecedents[self.calculerIndexCoord(suivant)]=noeud
        noeudFin = self.definirObjectif()[0]
        at = noeudFin
        if(noeudFin in self.NoeudsPrecedents):
            n=self.NoeudsPrecedents.index(noeudFin)
            while(at!=None):
                self.cheminASuivre.append(at)
                at=self.NoeudsPrecedents[self.calculerIndexCoord(at)]
            self.cheminASuivre.reverse()
            self.cheminASuivre.pop(0)
            if(self.cheminASuivre!=[]):
                coordVersQuiBouger = self.cheminASuivre[0]
                self.mouvement = [b-a for a,b in zip(self.position,coordVersQuiBouger)]
            else:
                self.mouvement=[0,0]
        else:
            self.mouvement=[0,0]

    def calculerIndexCoord(self, coord):
        return self.manoir.taille*coord[0]+coord[1]
    def calculerMouvement(self, coordVersQuiBouger):
        self.mouvement = [b-a for a,b in zip(self.position,coordVersQuiBouger)]

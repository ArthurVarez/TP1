# -*- coding: utf-8 -*-
from Capteur import *
from tkinter import *
from Effecteur import *
import math
import time
import threading
class Aspirateur(threading.Thread):
    def __init__(self,manoir, canvas):
        threading.Thread.__init__(self)
        self.aspi_icon = PhotoImage(file='../img/icons/roomba_f.png')
        self.canvas = canvas
        #### Environnemment
        self.manoir = manoir
        #### Mesure de performance
        self.consommation=0
        self.score=0

        #### Etats
        self.position=[0,0]
        self.positionsPoussieres=[]
        self.positionsBijoux=[]

        #### Mouvement désiré
        self.mouvement=[0,0]

        #### Effecteur et Capteur
        self.capteur = Capteur()
        self.effecteur = Effecteur()

        self.aspirateurDejaDessinee = 0
    def run(self):
        self.afficherAspirateur()
        while(1):
            self.capteur.capterEnvironnemment(self,self.manoir)
            if(self.manoirPropre()!=True):
                self.mouvement = self.prendreDecision()
                print("Le manoir est encore sale, je vais voir ce que je peux faire")
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
            self.consommation+=1
        time.sleep(1)

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
        time.sleep(1)

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


    def definirObjectif(self):
        distanceMin=math.inf
        coordPlusProche=self.position
        newDistanceMin=0
        for coord in self.positionsPoussieres:
            newDistanceMin=self.calculerDistanceEuclidienne(self.position,coord)
            if(newDistanceMin<distanceMin):
                distanceMin=newDistanceMin
                coordPlusProche=coord
        print("Je veux me déplacer vers "+str(coordPlusProche))
        return [coordPlusProche, distanceMin]

    def calculerDistanceEuclidienne(self, a, b):
        return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

    def manoirPropre(self):
        return self.positionsPoussieres==[]

    def aspirer(self):
        self.manoir.grille[self.position[0]][self.position[1]][0]=0
        self.consommation+=1
        indexPoussiere = self.position[0]*self.manoir.taille+self.position[1]
        self.canvas.delete(self.manoir.dicoPoussiere[indexPoussiere])
        print("J'aspire à la position "+str(self.position))
    def ramasserBijou(self):
        self.manoir.grille[self.position[0]][self.position[1]][1]=0
        self.consommation+=1
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


import random
from tkinter import *
import numpy as np
import time
import threading
class Manoir(threading.Thread):
    def __init__(self, taille, canvas):
        threading.Thread.__init__(self)
        self.taille=taille
        self.grille=[[[0,0] for i in range(taille)] for i in range(taille)]

        self.canvas = canvas
        self.dirt_icon = PhotoImage(file='../img/icons/dirt_f.png')
        self.diamond_icon = PhotoImage(file='../img/icons/diamond_f.png')
        self.bg_icon = PhotoImage(file='../img/icons/bg.png')

        self.dicoPoussiere = dict()
        self.dicoBijou = dict()
        self.matriceAdjacence = [[0 for i in range(taille*taille)] for j in range(taille*taille)]
        self.listeCouple = []
        self.poussieresDejaDessinees = [[0 for i in range(taille)] for j in range(taille)]
        self.BijouxDejaDessinees = [[0 for i in range(taille)] for j in range(taille)]
        for i in range(taille):
            for j in range(taille):
                for i1 in range(taille):
                    for j1 in range(taille):
                        if((abs(i-i1)==1 and j==j1) or (abs(j-j1)==1 and i==i1)):
                            self.matriceAdjacence[taille*i+j][taille*i1+j1]=1
                            self.listeCouple.append([[i,j],[i1,j1]])
        self.afficherGrille()
    def run(self):
        while(1):
            aleatoire=random.randint(0,19)
            if(aleatoire==0):
                self.ajouterPoussiere()
            elif(aleatoire==1):
                self.ajouterBijou()
            self.updateGrille()
            time.sleep(1)


    def ajouterPoussiere(self):
        posX=random.randint(0,self.taille-1)
        posY=random.randint(0,self.taille-1)
        self.grille[posX][posY][0]=1
    def ajouterBijou(self):
        posX=random.randint(0,self.taille-1)
        posY=random.randint(0,self.taille-1)
        self.grille[posX][posY][1]=1
    def supprimerPoussiere(self, posX, posY):
        self.grille[posX][posY][0]=0
    def supprimerBijou(self, posX, posY):
        self.grille[posX][posY][1]=0
    def caseSale(self, posX, posY):
        return self.grille[posX][posY][0]
    def caseBijou(self, posX, posY):
        return self.grille[posX][posY][1]

    def afficherGrille(self):
        for i in range(self.taille):
            for j in range(self.taille):
                self.canvas.create_image(70*i,70*j,anchor= NW,image=self.bg_icon)
                self.canvas.create_line(0,70*j,self.taille*70,70*j)
                self.canvas.create_line(70*i,0,70*i,self.taille*70)
                # if(self.caseSale(i,j)):
                #     self.canvas.create_image(70*i,70*j,anchor=NW,image=self.dirt_icon)
                # if(self.caseBijou(i,j)):
                #     self.canvas.create_image(70*i,70*j,anchor=NW,image=self.diamond_icon)
    def updateGrille(self):
        for i in range(self.taille):
            for j in range(self.taille):
                if(self.caseSale(i,j) and self.poussieresDejaDessinees[i][j]==0):
                    indexPoussiere=self.taille*i+j
                    id=self.canvas.create_image(70*i,70*j,anchor=NW,image=self.dirt_icon)
                    self.dicoPoussiere[indexPoussiere]=id
                    self.poussieresDejaDessinees[i][j]=1
                if(self.caseBijou(i,j) and self.BijouxDejaDessinees[i][j]==0):
                    indexBijou=self.taille*i+j
                    self.dicoBijou[indexBijou]=self.canvas.create_image(70*i,70*j,anchor=NW,image=self.diamond_icon)
                    self.BijouxDejaDessinees[i][j]=1
    def grille2(self):
        grille2=[[0 for k in range(self.taille)] for k in range(self.taille)]
        for i in range(self.taille):
            for j in range(self.taille):
                if (self.grille[i][j][0]==1 or self.grille[i][j][1]==1):
                    grille2[i][j]=1
        grille2=[list(i) for i in zip(*grille2)]
        return grille2

    def coordonnees(self):
        x,y=[],[]
        grille3=self.grille2()
        for i in range(self.taille):
            for j in range(self.taille):
                if (grille3[i][j]==1):
                    x.append(j+1)
                    y.append(i+1)
        return (x,y)

    def premier_parcour(self,posXaspi,posYaspi):
        (x,y)=self.coordonnees()
        coord=[[posXaspi,posYaspi]]
        l=[]
        liste_min=[]
        '''ecrire les coordonnees des xi et yi sous forme de sous liste [xi,yi]'''
        for i in range(len(x)):
            l+=[[x[i],y[i]]]
        'calcul de la distance euclidienne entre l(0) et l(i)'
        for j in range(len(x)):
          m=[]
          n=[]
          for u in range(1,len(l)):
                 m+=[[(l[u][0]-l[0][0]),(l[u][1]-l[0][1])]]
          for k in range(len(m)):
                      n+=[np.sqrt((m[k][0])**2+(m[k][1])**2)]
                      'recuperation de la distance minimale ainsi que son indice entre l(0) et l(i)'
                      minima=min(n)
                      indice = n.index(minima)
          'la liste liste_min contient ces distances minimales'
          liste_min+=[minima]
          'calcul de la somme de la distance finale entre l(0) et l(i)'
          somme_min=sum(liste_min)
          if len(l)>1:
            'la liste coord contient les differents coordonnees correspondant a ces distances minimales'
            coord+=[l[indice+1]]
            b=l.pop(0)
            b=l.insert(0,l[indice])
            b=l.pop(indice+1)
        return(coord,somme_min)




##    def parcoursPC(self, posAspi):
##        """ parcours profondeur utilise une fonction interne récursive"""
##        def parcoursR(posAspi):
##            if posAspi in visite:
##                return
##            else:
##                visite.append(posAspi)
##                for v in self.voisins(posAspi):
##                       if v not in L and v not in visite:
##                          L.append(v)
##                          chemin[v]=deepcopy(L)
##                       if v in self.ssas():
##                           for i in range(len(L)-1):
##                               a=L.pop(-1)
##                       parcoursR(v)
##        L=[posAspi]
##        visite = []
##        chemin = {}
##        chemin[posAspi] =[posAspi]
##        parcoursR(posAspi)
##        return chemin



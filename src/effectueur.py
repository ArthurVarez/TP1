from capteurs import Capteur


class Effectueur:
    def __init__(self,aspirateur,capteur):
        self.aspirateur = aspirateur
        self.capteur = capteur

    def Do(self,grid,position):
        if(self.capteur.IsBoth(grid,position)):
            grid[position[0]][position[1]][0] = 0
            grid[position[0]][position[1]][0] = 0
        else:
            if(self.capteur.IsDirt(grid,position)):
                grid[position[0]][position[1]][0] = 0
            if(self.capteur.IsBijou(grid,position)):
                grid[position[0]][position[1]][1] = 0



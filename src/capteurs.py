from typing import List


class Capteur:
    def __init__(self,aspirateur):
        self.aspirateur = aspirateur

    def IsDirt(self,grid,position):#ici postion est un liste [x,y]
        dirt = False
    
        if isinstance(self,position,list):
            if (grid[position[0]][position[1]][0]==1):
                dirt = True
        
        return dirt
    
    def IsBijou(grid,position):#ici postion est un liste [x,y]
        Bijou = False
        if isinstance(position,list):
            if (grid[position[0]][position[1]][1]==1):
                Bijou = True
        return Bijou
    def IsBoth(self,grid,position):#ici postion est un liste [x,y]
        return self.IsBijou(grid,position) & self.IsDirt(grid,position)

    

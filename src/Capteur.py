class Capteur:
    def capterEnvironnemment(self,aspirateur, manoir):
        positionsPoussieres = []
        positionsBijoux =[]
        taille = manoir.taille
        for i in range(taille):
            for j in range(taille):
                if(manoir.grille[i][j][0]==1):
                    positionsPoussieres.append([i,j])
                if(manoir.grille[i][j][1]==1):
                    positionsBijoux.append([i,j])
        aspirateur.positionsPoussieres = positionsPoussieres
        aspirateur.positionsBijoux = positionsBijoux

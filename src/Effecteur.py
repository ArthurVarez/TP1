class Effecteur:
    def effectuerMouvement(self,aspirateur, mouvement):
        test = [a + b for a,b in zip(aspirateur.position,mouvement)]
        aspirateur.position = [a + b for a,b in zip(aspirateur.position,mouvement)]
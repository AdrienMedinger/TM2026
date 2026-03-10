class Livre :
    def __init__(self,titre,auteur,etat) :
        self.titre = titre 
        self.auteur = auteur 
        self.etat = etat 

    def degrade (self):
        if self.etat > 0 :
            self.etat -=1
    

    def description (self) :
        print("Titre :",self.titre)
        print("Auteur :", self.auteur)
        print("Etat :", self.etat)


class Bibliothque :
    def __init__(self):
        self.livres = []

    def ajoute(self,livre):
        self.livres.append(livre)

    def supprimer(self,livre):
        for livre in self.livres :
            if livre.etat ==0 :
                self.livres.remove(livre)

    def inventaire(self) :
        for livre in self.livres :
            livre.description()
            print()
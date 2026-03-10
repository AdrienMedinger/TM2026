class Elève :
    def __init__(self,nom,classe,note):
        self.nom = nom 
        self.classe = classe
        self.note = note 

élève1 = Elève("Adrien",1,5)
élève2 = Elève("joachim",2,4)
elève3 = Elève("Antoine",3,6)

def comparaison(élève1, élève2) :
    if élève1.note > élève2.note :
       return élève1.nom
    
    else:
        return élève2.nom

print (comparaison(élève1, élève2))
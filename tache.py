import datetime as dt

#Classe Tâche
class Tache:
    def __init__(self,titre,description,priorite,id=None):
        self.id = id
        self.titre = titre
        self.description = description
        self.date = dt.date.today().strftime("%d/%m/%Y")
        self.statut = "à faire"
        self.priorite = priorite


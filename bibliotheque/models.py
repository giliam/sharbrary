from django.db import models
from datetime import datetime    

class Auteur(models.Model):
    prenom = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    annee_naissance = models.DateTimeField('birthdate')
    annee_mort = models.DateTimeField('date of death')
    date_ajout = models.DateTimeField('date added to the database',auto_now_add=True)

    def __unicode__(self):
        return self.prenom + " " + self.nom.upper()

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    annee_parution = models.DateTimeField('date published')
    date_ajout = models.DateTimeField('date added to the library',auto_now_add=True)
    auteur = models.ForeignKey(Auteur)

    def __unicode__(self):
        return self.titre

from django.db import models

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    annee_parution = models.DateTimeField('date published')
    date_ajout = models.DateTimeField('date added to the library')
    def __unicode__(self):
        return self.name
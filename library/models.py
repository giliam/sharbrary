from django.db import models
from datetime import datetime    

class Author(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    birthdate = models.DateTimeField('birthdate')
    death_date = models.DateTimeField('date of death')
    adding_date = models.DateTimeField('date added to the database',auto_now_add=True)

    def __unicode__(self):
        return self.firstname + " " + self.lastname.upper()

class Book(models.Model):
    title = models.CharField(max_length=200)
    publishing_date = models.DateTimeField('date published')
    adding_date = models.DateTimeField('date added to the library',auto_now_add=True)
    author = models.ForeignKey(Author)

    def __unicode__(self):
        return self.title

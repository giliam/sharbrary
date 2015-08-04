from django.db import models
from datetime import datetime    

class Author(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    birthdate = models.DateTimeField('birthdate',blank=True)
    death_date = models.DateTimeField('date of death',blank=True)
    added_date = models.DateTimeField('date added to the database',auto_now_add=True)
    updated_date = models.DateTimeField('date updated to the database',auto_now=True)

    def __unicode__(self):
        return self.firstname + " " + self.lastname.upper()

class Editor(models.Model):
    name = models.CharField(max_length=200)    
    added_date = models.DateTimeField('date added to the database',auto_now_add=True)
    updated_date = models.DateTimeField('date updated to the database',auto_now=True)

    def __unicode__(self):
        return "Editor: " + self.name

class Theme(models.Model):
    name = models.CharField(max_length=200)
    period = models.CharField(max_length=200,blank=True)
    added_date = models.DateTimeField('date added to the database',auto_now_add=True)
    updated_date = models.DateTimeField('date updated to the database',auto_now=True)

    def __unicode__(self):
        return "Theme: " + self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    publishing_date = models.DateTimeField('date published',blank=True)
    added_date = models.DateTimeField('date added to the library',auto_now_add=True)
    updated_date = models.DateTimeField('date updated to the database',auto_now=True)
    author = models.ForeignKey(Author,blank=True)
    themes = models.ManyToManyField(Theme,blank=True)
    summary = models.TextField(blank=True,default="")

    def __unicode__(self):
        return self.title

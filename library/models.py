from django.db import models
from datetime import datetime    
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class Author(models.Model):
    firstname = models.CharField(verbose_name=_('firstname'),max_length=200)
    lastname = models.CharField(verbose_name=_('lastname'),max_length=200)
    birthdate = models.DateTimeField(_('birthdate'),blank=True,null=True)
    death_date = models.DateTimeField(_('date of death'),blank=True,null=True)
    added_date = models.DateTimeField(_('date added to the database'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)

    def __unicode__(self):
        return self.firstname + " " + self.lastname.upper()

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

class Editor(models.Model):
    name = models.CharField(verbose_name=_('name'),max_length=200)    
    added_date = models.DateTimeField(_('date added to the database'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)

    def __unicode__(self):
        return _("Editor: ") + self.name

    class Meta:
        verbose_name = _("Editor")
        verbose_name_plural = _("Editors")

class Theme(models.Model):
    name = models.CharField(verbose_name=_('name'),max_length=200)
    period = models.CharField(verbose_name=_('period'),max_length=200,blank=True)
    added_date = models.DateTimeField(_('date added to the database'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)

    def __unicode__(self):
        return _("Theme: ") + self.name

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")

class Book(models.Model):
    title = models.CharField(verbose_name=_('title'),max_length=200)
    publishing_date = models.DateTimeField(_('date published'),blank=True,null=True)
    added_date = models.DateTimeField(_('date added to the library'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)
    owner = models.ForeignKey(User,blank=True,null=True,verbose_name=_('owner'))
    author = models.ForeignKey(Author,blank=True,null=True,verbose_name=_('author'))
    editor = models.ForeignKey(Editor,blank=True,null=True,verbose_name=_('editor'))
    themes = models.ManyToManyField(Theme,verbose_name=_('themes'),blank=True)
    summary = models.TextField(verbose_name=_('summary'),blank=True,default="")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

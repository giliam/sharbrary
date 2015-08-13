from django.db import models
from datetime import datetime    
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

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
        verbose_name = _("author")
        verbose_name_plural = _("authors")
        permissions = (
            ("author_new", "Add an author"),
            ("author_detail", "Show an author details"),
            ("author_edit", "Edit an author"),
            ("author_delete", "Delete an author"),
            ("author_list", "Show the list of authors"),
        )
        default_permissions = []

class Editor(models.Model):
    name = models.CharField(verbose_name=_('name'),max_length=200)    
    added_date = models.DateTimeField(_('date added to the database'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)

    def __unicode__(self):
        return _("editor") + " : " + self.name

    class Meta:
        verbose_name = _("editor")
        verbose_name_plural = _("editors")
        permissions = (
            ("editor_new", "Add an editor"),
            ("editor_edit", "Edit an editor"),
            ("editor_delete", "Delete an editor"),
            ("editor_list", "Show the list of editors"),
        )
        default_permissions = []

class Theme(models.Model):
    name = models.CharField(verbose_name=_('name'),max_length=200)
    added_date = models.DateTimeField(_('date added to the database'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)

    def __unicode__(self):
        return _("theme") + " : " + self.name

    class Meta:
        verbose_name = _("theme")
        verbose_name_plural = _("themes")
        permissions = (
            ("theme_new", "Add a theme"),
            ("theme_edit", "Edit a theme"),
            ("theme_delete", "Delete a theme"),
            ("theme_list", "Show the list of themes"),
        )
        default_permissions = []


class Period(models.Model):
    name = models.CharField(verbose_name=_('name'),max_length=200)
    added_date = models.DateTimeField(_('date added to the database'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)

    def __unicode__(self):
        return _("period") + " : " + self.name

    class Meta:
        verbose_name = _("period")
        verbose_name_plural = _("periods")
        permissions = (
            ("period_new", "Add a period"),
            ("period_edit", "Edit a period"),
            ("period_delete", "Delete a period"),
            ("period_list", "Show the list of periods"),
        )
        default_permissions = []

class Book(models.Model):
    title = models.CharField(verbose_name=_('title'),max_length=200)
    publishing_date = models.DateTimeField(_('date published'),blank=True,null=True)
    added_date = models.DateTimeField(_('date added to the library'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)
    owners = models.ManyToManyField(User,blank=True,verbose_name=_('owner'))
    author = models.ForeignKey(Author,blank=True,null=True,verbose_name=_('author'))
    editor = models.ForeignKey(Editor,blank=True,null=True,verbose_name=_('editor'))
    themes = models.ManyToManyField(Theme,verbose_name=_('themes'),blank=True)
    periods = models.ManyToManyField(Period,verbose_name=_('periods'),blank=True)
    summary = models.TextField(verbose_name=_('summary'),blank=True,default="")
    cover = models.ImageField(upload_to="cover/",verbose_name=_('cover'),null=True,blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")
        permissions = (
            ("book_new", "Add a book"),
            ("book_detail", "Show a book page"),
            ("book_edit", "Edit a book"),
            ("book_delete", "Delete a book"),
            ("book_remove_from_library", "Remove a book from your library"),
            ("book_remove_from_all_libraries", "Remove a book from all libraries"),
            ("book_list", "Show the list of books"),
        )
        default_permissions = []

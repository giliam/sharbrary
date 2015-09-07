# coding: utf-8
from django.db import models
from datetime import datetime    
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Opinion values
OPINION_NOTATION_VALUES = (
    (0, _('DO NOT READ IT')),
    (1, _('This is bad.')),
    (2, _('Humpf')),
    (3, _('Not so bad')),
    (4, _('Liked it!')),
    (5, _('READ IT')),
)

class Author(models.Model):
    firstname = models.CharField(verbose_name=_('firstname'),max_length=200)
    lastname = models.CharField(verbose_name=_('lastname'),max_length=200)
    birthdate = models.DateTimeField(_('birthdate'),blank=True,null=True)
    death_date = models.DateTimeField(_('date of death'),blank=True,null=True)
    added_date = models.DateTimeField(_('date added to the database'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)

    def save(self, *args, **kwargs):
        if(not self.birthdate or not self.death_date or self.birthdate < self.death_date):
            super(Author, self).save(*args, **kwargs)
        else:
            raise Exception, _("Death date should be greater than birthdate")

    def __unicode__(self):
        return self.firstname + " " + self.lastname.upper()

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")
        permissions = (
            ("author_new", "Add an author"),
            ("author_detail", "Show an author details"),
            ("author_edit", "Edit an author"),
            ("author_moderate", "Moderate an author"),
            ("author_delete", "Delete an author"),
            ("author_list", "Show the list of authors"),
        )
        default_permissions = []
        ordering = ['lastname', 'firstname']

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
            ("editor_moderate", "Moderate an editor"),
            ("editor_delete", "Delete an editor"),
            ("editor_list", "Show the list of editors"),
        )
        default_permissions = []
        ordering = ['name']

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
            ("theme_moderate", "Moderate a theme"),
            ("theme_delete", "Delete a theme"),
            ("theme_list", "Show the list of themes"),
        )
        default_permissions = []
        ordering = ['name']


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
            ("period_moderate", "Moderate a period"),
            ("period_delete", "Delete a period"),
            ("period_list", "Show the list of periods"),
        )
        default_permissions = []
        ordering = ['name']

class Book(models.Model):
    title = models.CharField(verbose_name=_('title'),max_length=200)
    publishing_date = models.DateTimeField(_('date published'),blank=True,null=True)
    added_date = models.DateTimeField(_('date added to the library'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)
    author = models.ForeignKey(Author,blank=True,null=True,verbose_name=_('author'))
    themes = models.ManyToManyField(Theme,verbose_name=_('themes'),blank=True)
    periods = models.ManyToManyField(Period,verbose_name=_('periods'),blank=True)
    
    editor = models.ForeignKey(Editor,blank=True,null=True,verbose_name=_('editor'))
    cover = models.ImageField(upload_to="cover/",verbose_name=_('cover'),null=True,blank=True)
    summary = models.TextField(verbose_name=_('summary'),blank=True,default="")

    owners = models.ManyToManyField(User,blank=True,verbose_name=_('owner'),through="Ownership",related_name="+")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")
        permissions = (
            ("book_new", "Add a book"),
            ("book_detail", "Show a book page"),
            ("book_edit", "Edit a book"),
            ("book_moderate", "Moderate a book"),
            ("book_delete", "Delete a book"),
            ("book_remove_from_library", "Remove a book from your library"),
            ("book_remove_from_all_libraries", "Remove a book from all libraries"),
            ("book_list", "Show the list of books"),
        )
        default_permissions = []
        ordering = ['title']


class Ownership(models.Model):
    book = models.ForeignKey(Book,verbose_name=_('book'))
    owner = models.ForeignKey(User,verbose_name=_('owner'))
    copies = models.PositiveIntegerField(default=1,verbose_name=_('number of copies'),blank=True)

    added_date = models.DateTimeField(_('date added to the library'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)
    
    editor = models.ForeignKey(Editor,blank=True,null=True,verbose_name=_('editor'))
    comments = models.TextField(verbose_name=_('comments'),blank=True,default="")
    cover = models.ImageField(upload_to="cover/",verbose_name=_('cover'),null=True,blank=True)

    def __unicode__(self):
        return _("%(book)s owned by %(owner)s") % {'book':self.book, 'owner':self.owner.username} 

    class Meta:
        verbose_name = _("ownership")
        verbose_name_plural = _("ownerships")
        permissions = (
            ("ownership_new", "Have a book"),
            ("ownership_edit", "Edit a ownership"),
            ("ownership_moderate", "Moderate a ownership"),
            ("ownership_delete", "Delete a ownership"),
        )
        default_permissions = []
        ordering = ['book__title','owner__username']


class Opinion(models.Model):
    book = models.ForeignKey(Book,verbose_name=_('book'))
    author = models.ForeignKey(User,verbose_name=_('author'))
    
    added_date = models.DateTimeField(_('date added'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)

    value = models.PositiveIntegerField(choices=OPINION_NOTATION_VALUES)

    def __unicode__(self):
        return _("%(author)s rated %(book)s of %(value)s") % {'book':self.book, 'author':self.author.username, 'value':self.value}

    class Meta:
        verbose_name = _("opinion")
        verbose_name_plural = _("opinions")
        permissions = (
            ("opinion_new", "Have an opinion"),
            ("opinion_edit", "Edit an opinion"),
            ("opinion_moderate", "Moderate an opinion"),
            ("opinion_delete", "Delete an opinion"),
        )
        default_permissions = []
        ordering = ['book__title','author__username']

class Page(models.Model):
    name = models.CharField(max_length=200,verbose_name=_('name of the page'))
    title = models.CharField(max_length=200,verbose_name=_('title of the page'))
    content = models.TextField(verbose_name=_('content of the page'),default="")

    def __unicode__(self):
        return _("Page %(name)s") % {'name':self.name}

    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("pages")
        permissions = (
            ("page_new", "Create a page"),
            ("page_edit", "Edit a page"),
            ("page_moderate", "Moderate a page"),
            ("page_delete", "Delete a page"),
        )
        default_permissions = []
        ordering = ['name']
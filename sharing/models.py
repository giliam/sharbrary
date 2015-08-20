# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone

from library.models import Book

class Profile(models.Model):
    user = models.OneToOneField(User)
    informations = models.TextField(blank=True,verbose_name=_("informations"))
    phone_regex = RegexValidator(regex=r'^(\d{2}( |-)?){5}$', message=_("Phone number must be entered in the format: '0123456789'. Up to 10 digits allowed."))
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=25,verbose_name=_("phone number"))

    def __unicode__(self):
        return u"Profile of {0}".format(self.user.username)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        permissions = (
            ("profile_new", "Add a profile"),
            ("profile_edit", "Edit a profile"),
            ("profile_delete", "Delete a profile"),
            ("profile_list", "Show the list of profiles"),
            ("profile_show", "Show a profile"),
        )
        default_permissions = []

class Lending(models.Model):
    borrower = models.ForeignKey(User,blank=True,verbose_name=_("borrower"))
    book = models.ForeignKey(Book,verbose_name=_("book"))
    beginning_date = models.DateTimeField(_('beginning date of the lending'),blank=True,null=True,default=timezone.now)
    end_date = models.DateTimeField(_('end date of the lending'),blank=True,null=True)
    added_date = models.DateTimeField(_('date added to the database'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated to the database'),auto_now=True)

    def save(self, *args, **kwargs):
        if(not self.end_date or self.end_date >= self.beginning_date):
            super(Lending, self).save(*args, **kwargs)
        else:
            raise Exception, _("The end date must be after the beginning date.")

    def __unicode__(self):
        return unicode(self.borrower) + u" borrowed " + unicode(self.book)

    class Meta:
        verbose_name = _("lending")
        verbose_name_plural = _("lendings")
        permissions = (
            ("lending_new", "Add a lending"),
            ("lending_edit", "Edit a lending"),
            ("lending_delete", "Delete a lending"),
            ("lending_list", "Show the list of lendings"),
        )
        default_permissions = []
# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# STATUS POSSIBLE
STATUS_OPEN = 'OP'
STATUS_CLOSED = 'CL'
STATUS_DELETED = 'DE'
STATUS_ARCHIVED = 'AR'
STATUS_POSSIBILITIES = (
    ('OP', 'OPEN'),
    ('CL', 'CLOSED'),
    ('DE', 'DELETED'),
    ('AR', 'ARCHIVED'),
)


class Discussion(models.Model):
    title = models.CharField(verbose_name=_('title'),max_length=200)
    
    added_date = models.DateTimeField(_('date added'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated'),auto_now=True)
    
    author = models.ForeignKey(User,blank=True,null=True,verbose_name=_('author'))
    
    status = models.CharField(verbose_name=_('status of the topic'),max_length=200,choices=STATUS_POSSIBILITIES,default=STATUS_OPEN)
    
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("discussion")
        verbose_name_plural = _("discussions")
        permissions = (
            ("discussion_new", "Add an discussion"),
            ("discussion_detail", "Show a discussion details"),
            ("discussion_edit", "Edit a discussion"),
            ("discussion_delete", "Delete a discussion"),
            ("discussion_list", "Show the list of discussions"),
        )
        default_permissions = []
        ordering = ['-updated_date', 'title']

class Message(models.Model):
    discussion = models.ForeignKey(Discussion, related_name="messages")
    message = models.TextField(verbose_name=_('message'))
    
    added_date = models.DateTimeField(_('date added'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated'),auto_now=True)
    
    author = models.ForeignKey(User,blank=True,null=True,verbose_name=_('author'))

    def __unicode__(self):
        return self.message[:10]

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
        permissions = (
            ("message_new", "Add an message"),
            ("message_detail", "Show a message details"),
            ("message_edit", "Edit a message"),
            ("message_delete", "Delete a message"),
            ("message_list", "Show the list of messages"),
        )
        default_permissions = []
        ordering = ['-added_date']
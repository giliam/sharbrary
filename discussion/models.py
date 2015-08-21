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

class Message(models.Model):
    discussion = models.ManyToManyField(Discussion, related_name="messages")
    message = models.TextField(verbose_name=_('message'))
    
    added_date = models.DateTimeField(_('date added'),auto_now_add=True)
    updated_date = models.DateTimeField(_('date updated'),auto_now=True)
    
    author = models.ForeignKey(User,blank=True,null=True,verbose_name=_('author'))


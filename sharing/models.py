from django.db import models
from django.contrib.auth.models import User
from library.models import Book

class Lending(models.Model):
    borrower = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    status = models.BooleanField(default=False)
    beginning_date = models.DateTimeField('beginning date of the lending',blank=True,null=True)
    end_date = models.DateTimeField('end date of the lending',blank=True,null=True)
    added_date = models.DateTimeField('date added to the database',auto_now_add=True)
    updated_date = models.DateTimeField('date updated to the database',auto_now=True)

    def __unicode__(self):
        return self.borrower + " borrowed " + self.book
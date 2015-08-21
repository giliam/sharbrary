# coding: utf-8
from django.db.models import Q
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from sharing.models import Lending

def determine_book_availability(beginning_date,book_copy):
    lendings = Lending.objects.filter(Q(beginning_date__lte=beginning_date,end_date__gte=beginning_date,book_copy__id=book_copy.id)|Q(beginning_date__lte=beginning_date,end_date=None,book_copy__id=book_copy.id))
    return lendings

def determine_conflicts_with_next_lendings(beginning_date,book_copy):
    lendings = Lending.objects.filter(Q(beginning_date__gte=beginning_date,book_copy__id=book_copy.id))
    return lendings


def is_lending_possible(beginning_date,book_copy):
    current_lendings = determine_book_availability(beginning_date,book_copy)
    if current_lendings:
        raise ValidationError(_("This book is already borrowed ! (borrowed by %(lendings)s)") % { 'lendings': ' ,'.join([flending.borrower.username for flending in current_lendings.all()])} )
        return False

    future_lendings = determine_conflicts_with_next_lendings(beginning_date,book_copy)
    if future_lendings:
        raise ValidationError(_("You chose a past date whereas the book is now borrowed which is not possible ! (borrowed by %(lendings)s)") % { 'lendings': ' ,'.join([flending.borrower.username for flending in future_lendings.all()])} )
        return False
    
    return True
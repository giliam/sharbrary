# coding: utf-8
from django.db.models import Q

from sharing.models import Lending

def determine_book_availability(beginning_date,book):
    lendings = Lending.objects.filter(Q(beginning_date__lte=beginning_date,end_date__gte=beginning_date,book__id=book.id)|
        Q(beginning_date__lte=beginning_date,end_date=None,book__id=book.id))
    return lendings
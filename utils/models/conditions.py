# coding: utf-8
from django.db.models import Q
from django.utils import timezone

def actual_lending():
	return Q(beginning_date__lte=timezone.now(),end_date__isnull=True)|Q(end_date__gte=timezone.now(),beginning_date__isnull=True)|Q(beginning_date__lte=timezone.now(),end_date__gte=timezone.now())
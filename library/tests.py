# coding: utf-8
from django.test import TestCase
from library.models import Author
from django.utils import timezone
import datetime

class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create(firstname="John", lastname="Keats")
        Author.objects.create(firstname="Victor", lastname="Hugo")
        Author.objects.create(firstname="Honoré", lastname="Balzac")
        Author.objects.create(firstname="Gustave", lastname="Flaubert")
        Author.objects.create(firstname="Emile", lastname="Zola")

    def test_birthdate_before_deathdate(self):
        """Author birthdate must be before deathdate"""
        author = Author.objects.get(firstname="John", lastname="Keats")
        author.birthdate = timezone.make_aware(datetime.datetime(1979,10,12))
        author.deathdate = timezone.make_aware(datetime.datetime(1952,11,03))
        self.assertRaises(Exception, author.save())

    def test_no_birthdate(self):
        """Author birthdate must be before deathdate"""
        author = Author.objects.get(firstname="Emile", lastname="Zola")
        author.birthdate = None
        author.deathdate = timezone.make_aware(datetime.datetime(1952,11,03))
        self.assertRaises(Exception, author.save())

    def test_no_deathdate(self):
        """Author birthdate must be before deathdate"""
        author = Author.objects.get(firstname="Emile", lastname="Zola")
        author.birthdate = timezone.make_aware(datetime.datetime(1952,11,03))
        author.deathdate = None
        self.assertRaises(Exception, author.save())
# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse

from library.models import Author
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

class OwnershipTestCase(TestCase):
    def setUp(self):
        self.bob = User.objects.create_superuser('bob', 'bob@test.fr', 'blob')
        self.bib = User.objects.create_user('bib', 'bib@test.fr', 'blib')
        self.bab = User.objects.create_user('bab', 'bab@test.fr', 'blab')
        self.bub = User.objects.create_user('bub', 'bub@test.fr', 'blub')
        self.beb = User.objects.create_user('beb', 'beb@test.fr', 'bleb')

    def test_book_new_owners(self):
        """Test if the creation of a book creates the ownerships associated"""
        self.client.login(username='bob', password='blob')
        data = {
            'title': 'An interesting test book',
            'owners': {
                    self.bob.id, self.bib.id, self.bab.id
                    },
        }

        response = self.client.post(reverse('book_new'), data)
        self.assertEqual(response.status_code, 302)
        # Then check if the book has been created
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'An interesting test book')
        self.assertQuerysetEqual(response.context['book'].owners.order_by('id').all(),[repr(self.bob), repr(self.bib), repr(self.bab)])
        self.client.logout()
        
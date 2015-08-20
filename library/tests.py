# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.db.models import Q

from utils.groups.create_groups import add_perms_to_person, AUTHORIZED_READONLY_MODELS, AUTHORIZED_STANDARD_MODELS

from library.models import Book, Author, Ownership
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
        perms = Permission.objects.filter(Q(content_type__app_label='library')|Q(content_type__app_label='sharing'))
        self.bob = User.objects.create_superuser('bob', 'bob@test.fr', 'blob')
        self.bib = User.objects.create_user('bib', 'bib@test.fr', 'blib')
        self.bab = User.objects.create_user('bab', 'bab@test.fr', 'blab')
        self.bub = User.objects.create_user('bub', 'bub@test.fr', 'blub')

        add_perms_to_person(self.bib,perms,AUTHORIZED_STANDARD_MODELS)
        add_perms_to_person(self.bab,perms,AUTHORIZED_STANDARD_MODELS)
        add_perms_to_person(self.bub,perms,AUTHORIZED_READONLY_MODELS)

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
        # self.assertRedirects(response, reverse('book_detail',args=[1]))
        # Then check if the book has been created
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,data['title'])
        self.assertQuerysetEqual(response.context['book'].owners.order_by('id').all(),[repr(self.bob), repr(self.bib), repr(self.bab)])
        self.client.logout()
        
    def test_ownership_new(self):
        """Test if the ownership works"""

        pass

    def test_book_remove_from_my_library_not_mine(self):
        self.client.login(username='bib', password='blib')
        
        book = Book(title="The Hitchhiker's guide to Django Unit Tests")
        book.save()

        ownership = Ownership(book=book,owner=self.bob)
        ownership.save()

        response = self.client.get(reverse('book_remove_from_library',kwargs={'book_id':book.id}))
        print response.url
        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_book_remove_from_my_library(self):
        self.client.login(username='bib', password='blib')
        
        book = Book(title="The Hitchhiker's guide to bloblob Tests")
        book.save()

        ownership = Ownership(book=book,owner=self.bob)
        ownership.save()
        ownership = Ownership(book=book,owner=self.bib)
        ownership.save()

        response = self.client.get(reverse('book_remove_from_library',kwargs={'book_id':book.id}))
        print response.url
        self.assertEqual(response.status_code, 302)

        self.client.logout()

    def test_book_no_owners(self):
        self.client.login(username='bib', password='blib')
        
        book = Book(title="The Bloubiboulga's guide to bloblob Tests")
        book.save()

        response = self.client.get(reverse('book_remove_from_library',kwargs={'book_id':book.id}))
        print response.url
        self.assertEqual(response.status_code, 404)
        self.client.logout()
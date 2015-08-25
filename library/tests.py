# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils import translation

from utils.groups.create_groups import add_perms_to_person, AUTHORIZED_READONLY_MODELS, AUTHORIZED_STANDARD_MODELS

from library.models import Book, Author, Ownership, Editor, Theme, Period
from library.views import determine_new_ownership_necessary

import datetime

class AuthorTestCase(TestCase):
    def setUp(self):
        self.bob = User.objects.create_superuser('bob', 'bob@test.fr', 'blob')
        self.author_keats = Author.objects.create(firstname="John", lastname="Keats")
        self.author_zola = Author.objects.create(firstname="Emile", lastname="Zola")

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

    def test_creation(self):
        self.client.login(username='bob', password='blob')
        data = {
            'firstname': 'Robert',
            'lastname': 'Dure',
            'birthdate': '1950-06-01',
            'death_date': '1979-01-02',
        }

        response = self.client.post(reverse('author_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('author_list'))

        try:
            author = Author.objects.get(**data)
        except Author.DoesNotExist:
            author = None    
        self.assertIsNotNone(author)
        # Then check if the book has been created
        response = self.client.get(reverse('author_list'))
        self.assertQuerysetEqual(response.context['authors'].all(),[repr(author), repr(self.author_keats), repr(self.author_zola)])
        self.client.logout()

    def test_deletion(self):
        self.client.login(username='bob', password='blob')
        data = {
            'firstname': 'Robert',
            'lastname': 'Dure',
            'birthdate': '1950-06-01',
            'death_date': '1979-01-02',
        }
        author = Author.objects.create(**data)
        
        response = self.client.get(reverse('author_list'))
        self.assertQuerysetEqual(response.context['authors'].all(),[repr(author),repr(self.author_keats), repr(self.author_zola)])
        
        response = self.client.post(reverse('author_delete',args=[author.id]),{})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('author_list'))
        try:
            author = Author.objects.get(**data)
        except Author.DoesNotExist:
            author = None    
        self.assertIsNone(author)
        # Then check if the book has been created
        response = self.client.get(reverse('author_list'))
        self.assertQuerysetEqual(response.context['authors'].all(),[repr(self.author_keats), repr(self.author_zola)])
        self.client.logout()

    def test_update(self):
        self.client.login(username='bob', password='blob')
        data = {
            'firstname': 'Robert',
            'lastname': 'Dure',
            'birthdate': '1950-06-01',
            'death_date': '1979-01-02',
        }
       
        response = self.client.post(reverse('author_edit',args=[self.author_keats.id]),data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('author_list'))
        try:
            author = Author.objects.get(**data)
        except Author.DoesNotExist:
            author = None    
        self.assertIsNotNone(author)
        self.client.logout()



class EditorTestCase(TestCase):
    def setUp(self):
        self.bob = User.objects.create_superuser('bob', 'bob@test.fr', 'blob')

    def test_creation(self):
        self.client.login(username='bob', password='blob')
        data = {
            'name': 'Gallimard',
        }

        response = self.client.post(reverse('editor_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('editor_list'))

        try:
            editor = Editor.objects.get(**data)
        except Editor.DoesNotExist:
            editor = None    
        self.assertIsNotNone(editor)
        # Then check if the book has been created
        response = self.client.get(reverse('editor_list'))
        self.assertQuerysetEqual(response.context['editors'].all(),[repr(editor)])
        self.client.logout()

    def test_deletion(self):
        self.client.login(username='bob', password='blob')
        editor = Editor.objects.create(name='Dargaud')
        
        response = self.client.get(reverse('editor_list'))
        self.assertQuerysetEqual(response.context['editors'].all(),[repr(editor)])
        
        response = self.client.post(reverse('editor_delete',args=[editor.id]),{})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('editor_list'))
        try:
            editor = Editor.objects.get(name="Dargaud")
        except Editor.DoesNotExist:
            editor = None    
        self.assertIsNone(editor)
        # Then check if the book has been created
        response = self.client.get(reverse('editor_list'))
        self.assertQuerysetEqual(response.context['editors'].all(),[])
        self.client.logout()

    def test_update(self):
        self.client.login(username='bob', password='blob')
        editor = Editor.objects.create(name='Dargaud')
        data = {
            'name': 'La pleiade',
        }
       
        response = self.client.post(reverse('editor_edit',args=[editor.id]),data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('editor_list'))
        try:
            editor = Editor.objects.get(**data)
        except Editor.DoesNotExist:
            editor = None    
        self.assertIsNotNone(editor)
        self.client.logout()

class OwnershipTestCase(TestCase):
    def setUp(self):
        translation.activate("en")

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

        try:
            book = Book.objects.get(title="An interesting test book")
        except Book.DoesNotExist:
            book = None    
        self.assertIsNotNone(book)
        self.assertRedirects(response, reverse('book_detail',args=[book.id]))
        
        # Then check if the book has been created
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,data['title'])
        self.assertQuerysetEqual(response.context['book'].owners.order_by('id').all(),[repr(self.bob), repr(self.bib), repr(self.bab)])
        self.client.logout()
        
    def test_ownership_new_no_ownership(self):
        """Test the algorithm determining if a new ownership is necessary"""
        book = Book(title="Some annoying book")
        book.save()
        ownership = Ownership(book=book,owner=self.bib)
        self.assertTrue(determine_new_ownership_necessary(ownership,None))

    def test_ownership_new_other_ownership_someone_else(self):
        """Test the algorithm determining if a new ownership is necessary"""
        book = Book(title="Some annoying book")
        book.save()
        ownership = Ownership(book=book,owner=self.bib)
        existing_ownership = Ownership(book=book,owner=self.bob)
        self.assertTrue(determine_new_ownership_necessary(ownership,existing_ownership))

    def test_ownership_new_other_ownership(self):
        """Test the algorithm determining if a new ownership is necessary"""
        book = Book(title="Some annoying book")
        book.save()
        ownership = Ownership(book=book,owner=self.bib)
        existing_ownership = Ownership(book=book,owner=self.bib,copies=15)
        existing_ownership.save()
        self.assertFalse(determine_new_ownership_necessary(ownership,existing_ownership))

    def test_add_book_no_ownership(self):
        """Test the view adding a book to a library"""
        self.client.login(username='bib', password='blib')
        book = Book(title="Some really annoying book")
        book.save()

        data = {
            'copies':10,
        }

        response = self.client.post(reverse('book_add_this_to_my_library',kwargs={'book_id':book.id}),data)
        
        self.assertEqual(response.status_code, 302)     
        
        try:
            ownership = Ownership.objects.get(owner__id=self.bib.id,book__id=book.id)
        except Ownership.DoesNotExist:
            ownership = None

        self.assertIsNotNone(ownership)
        self.assertRedirects(response, reverse('book_detail',args=[book.id]))

        self.client.logout()

    def test_add_book_other_ownership_someone_else(self):
        """Test the view adding a book to a library"""
        self.client.login(username='bib', password='blib')
        book = Book(title="Some really annoying book")
        book.save()
        existing_ownership = Ownership(owner=self.bob,book=book,copies=10)
        existing_ownership.save()

        data = {
            'copies':42,
        }

        response = self.client.post(reverse('book_add_this_to_my_library',kwargs={'book_id':book.id}),data)
        
        self.assertEqual(response.status_code, 302)     
        
        try:
            ownership = Ownership.objects.get(owner__id=self.bib.id,book__id=book.id)
        except Ownership.DoesNotExist:
            ownership = None

        self.assertIsNotNone(ownership)
        self.assertRedirects(response, reverse('book_detail',args=[book.id]))

        response = self.client.get(reverse('book_detail',args=[book.id]))
        self.assertContains(response, self.bob.username.title() + " (" + str(existing_ownership.copies) + ")")
        self.assertContains(response, self.bib.username.title() + " (" + str(data['copies']) + ")")
        
        self.client.logout()

    def test_add_book_new_other_ownership(self):
        """Test the view adding a book to a library"""
        self.client.login(username='bib', password='blib')
        book = Book(title="Some really annoying book")
        book.save()
        existing_ownership = Ownership(owner=self.bib,book=book,copies=10)
        existing_ownership.save()

        data = {
            'copies':42,
        }

        response = self.client.post(reverse('book_add_this_to_my_library',kwargs={'book_id':book.id}),data)
        
        self.assertEqual(response.status_code, 302)     
        
        try:
            ownership = Ownership.objects.get(owner__id=self.bib.id,book__id=book.id)
        except Ownership.DoesNotExist:
            ownership = None

        self.assertIsNotNone(ownership)
        self.assertEqual(ownership.id,existing_ownership.id)
        self.assertRedirects(response, reverse('book_detail',args=[book.id]))

        response = self.client.get(reverse('book_detail',args=[book.id]))
        self.assertContains(response, self.bib.username.title() + " (" + str(existing_ownership.copies+data['copies']) + ")")
        
        self.client.logout()


    def test_book_remove_from_my_library_not_mine(self):
        self.client.login(username='bib', password='blib')
        
        book = Book(title="The Hitchhikers guide to Django Unit Tests without special caracter")
        book.save()

        book.owners.clear()
        ownership = Ownership(book=book,owner=self.bob)
        ownership.save()

        response = self.client.get(reverse('book_remove_from_library',kwargs={'book_id':book.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_list'))

        self.client.logout()

    def test_book_remove_from_my_library(self):
        self.client.login(username='bib', password='blib')
        
        book = Book(title="The Hitchhikers guide to bloblob Tests without special caracter")
        book.save()

        ownership = Ownership(book=book,owner=self.bob)
        ownership.save()
        ownership = Ownership(book=book,owner=self.bib)
        ownership.save()

        response = self.client.get(reverse('book_remove_from_library',kwargs={'book_id':book.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure you want to delete \"%(object)s\" ?" % {'object':book.title})

        self.client.logout()

    def test_book_no_owners(self):
        self.client.login(username='bib', password='blib')
        
        book = Book(title="The Bloubiboulga's guide to bloblob Tests")
        book.save()

        response = self.client.get(reverse('book_remove_from_library',kwargs={'book_id':book.id}))
        self.assertEqual(response.status_code, 404)
        self.client.logout()
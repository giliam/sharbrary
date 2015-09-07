# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.forms import ValidationError

from utils.tests.common_test_case import CommonTestCase, with_login_user

from library.models import Book, Ownership
from sharing.models import Profile, Lending, Queue

class LendingTestCase(CommonTestCase):
    def setUp(self):
        super(LendingTestCase,self).setUp()
        self.book = Book.objects.create(title='La vie et le reste')
        self.book_copy = Ownership.objects.create(book=self.book,owner=self.bob)

    @with_login_user('bob')
    def test_creation(self):
        data = {
            'borrower': self.bib.id,
            'book_copy': self.book_copy.id,
            'beginning_date': '2015-09-03 11:43',
        }

        response = self.client.post(reverse('lending_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_detail',args=[self.book.id]))

        try:
            lending = Lending.objects.get(**data)
        except Lending.DoesNotExist:
            lending = None    
        self.assertIsNotNone(lending)
        
        # Then check if the book has been created
        response = self.client.get(reverse('book_detail',args=[self.book.id]))
        self.assertQuerysetEqual(response.context['lendings'].all(),[repr(lending)])

    @with_login_user('bob')
    def test_creation_not_available(self):
        data = {
            'borrower': self.bib.id,
            'beginning_date': '2015-09-03 11:43',
        }
        # Create one lending which borrows all copies.
        lending = Lending.objects.create(beginning_date="2015-09-03",book_copy=self.book_copy,borrower=self.bob)

        # Tries to borrow the book anyway.
        try:
            response = self.client.post(reverse('lend_book',args=[self.book_copy.id]), data)
        except Exception:
            self.assertRaises(ValidationError)
            response = None
        self.assertIsNone(response)

        try:
            lending = Lending.objects.get(book_copy=self.book_copy.id,**data)
        except Lending.DoesNotExist:
            lending = None    
        self.assertIsNone(lending)
        

    @with_login_user('bub')
    def test_creation_no_right(self):
        response = self.client.post(reverse('lending_new'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sharing/login/?next=' + reverse('lending_new'))

    @with_login_user('bob')
    def test_deletion(self):
        lending = Lending.objects.create(beginning_date="2015-09-03",book_copy=self.book_copy,borrower=self.bob)
        
        response = self.client.get(reverse('book_detail',args=[self.book.id]))
        self.assertQuerysetEqual(response.context['lendings'].all(),[repr(lending)])
        
        response = self.client.post(reverse('lending_delete',args=[lending.id]),{})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lending_list'))
        try:
            lending = Lending.objects.get(book_copy=self.book_copy,borrower=self.bob)
        except Lending.DoesNotExist:
            lending = None    
        self.assertIsNone(lending)
        # Then check if the book has been created
        response = self.client.get(reverse('book_detail',args=[self.book.id]))
        self.assertQuerysetEqual(response.context['lendings'].all(),[])

    @with_login_user('bub')
    def test_deletion_no_right(self):
        lending = Lending.objects.create(beginning_date="2015-09-03",book_copy=self.book_copy,borrower=self.bub)
        response = self.client.post(reverse('lending_delete',args=[lending.id]),{})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sharing/login/?next=' + reverse('lending_delete',args=[lending.id]))

    @with_login_user('bib')
    def test_deletion_not_my_lending(self):
        lending = Lending.objects.create(beginning_date="2015-09-03",book_copy=self.book_copy,borrower=self.bob)
        response = self.client.post(reverse('lending_delete',args=[lending.id]),{})
        # only moderators can delete lendings
        self.assertEqual(response.status_code, 403)

    @with_login_user('bib')
    def test_end_lending(self):
        lending = Lending.objects.create(beginning_date="2015-09-03",book_copy=self.book_copy,borrower=self.bib)
        data = {
            'end_date':'2015-09-04',
        }
       
        response = self.client.post(reverse('lending_end',args=[lending.id]),data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_detail',args=[self.book.id]))
        try:
            lending = Lending.objects.get(**data)
        except Lending.DoesNotExist:
            lending = None    
        self.assertIsNotNone(lending)

    @with_login_user('bib')
    def test_end_lending_before_beginning(self):
        lending = Lending.objects.create(beginning_date="2015-09-03",book_copy=self.book_copy,borrower=self.bib)
        data = {
            'end_date':'2015-08-04',
        }
       
        response = self.client.post(reverse('lending_end',args=[lending.id]),data)
        self.assertEqual(response.status_code, 200)
        try:
            lending = Lending.objects.get(**data)
        except Lending.DoesNotExist:
            lending = None    
        self.assertIsNone(lending)

    @with_login_user('bib')
    def test_end_not_my_lending(self):
        lending = Lending.objects.create(beginning_date="2015-09-03",book_copy=self.book_copy,borrower=self.bob)
        data = {
            'end_date':'2015-09-04',
        }
       
        response = self.client.post(reverse('lending_edit',args=[lending.id]),data)
        self.assertEqual(response.status_code, 403)
        try:
            lending = Lending.objects.get(book_copy=self.book_copy,**data)
        except Lending.DoesNotExist:
            lending = None    
        self.assertIsNone(lending)

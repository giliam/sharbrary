# coding: utf-8
from django.utils import translation
from django.test import TestCase
from django.db.models import Q
from django.contrib.auth.models import User, Permission

from utils.groups.create_groups import add_perms_to_person, AUTHORIZED_READONLY_MODELS, AUTHORIZED_STANDARD_MODELS

class CommonTestCase(TestCase):
    def setUp(self):
        translation.activate("en")

        perms = Permission.objects.filter(Q(content_type__app_label='library')|Q(content_type__app_label='discussion')|Q(content_type__app_label='sharing'))
        self.bob = User.objects.create_superuser('bob', 'bob@test.fr', 'bob')
        self.bib = User.objects.create_user('bib', 'bib@test.fr', 'bib')
        self.bab = User.objects.create_user('bab', 'bab@test.fr', 'bab')
        self.bub = User.objects.create_user('bub', 'bub@test.fr', 'bub')

        add_perms_to_person(self.bib,perms,AUTHORIZED_STANDARD_MODELS)
        add_perms_to_person(self.bab,perms,AUTHORIZED_STANDARD_MODELS)
        add_perms_to_person(self.bub,perms,AUTHORIZED_READONLY_MODELS)

# Creates a decorator for functions.
def with_login_user(username_="bob",password_=False):
    def wrapper_creator(func):
        def wrapped(self, *args, **kwargs):
            # Default password is the username
            if not password_ or password_ is None:
                password = username_
            else:
                password = password_
            # Login
            self.client.login(username=username_,password=password)
            return func(self, *args, **kwargs)
        return wrapped
    return wrapper_creator
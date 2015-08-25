# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

from utils.tests.common_test_case import CommonTestCase

from discussion.models import Discussion

class DiscussionTestCase(CommonTestCase):
    def test_creation(self):
        self.client.login(username='bob', password='bob')
        data = {
            'title': 'Sujet de conversation',
        }

        response = self.client.post(reverse('discussion_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('discussion_list'))

        try:
            discussion = Discussion.objects.get(**data)
        except Discussion.DoesNotExist:
            discussion = None    
        self.assertIsNotNone(discussion)
        # Then check if the book has been created
        response = self.client.get(reverse('discussion_list'))
        self.assertQuerysetEqual(response.context['discussions'].all(),[repr(discussion)])
        self.client.logout()

    def test_creation_no_right(self):
        self.client.login(username='bub', password='bub')
        response = self.client.post(reverse('discussion_new'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sharing/login/?next=/discussion/discussion/new')
        self.client.logout()

    def test_deletion(self):
        self.client.login(username='bob', password='bob')
        discussion = Discussion.objects.create(title='La vie et le reste')
        
        response = self.client.get(reverse('discussion_list'))
        self.assertQuerysetEqual(response.context['discussions'].all(),[repr(discussion)])
        
        response = self.client.post(reverse('discussion_delete',args=[discussion.id]),{})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('discussion_list'))
        try:
            discussion = Discussion.objects.get(title="La vie et le reste")
        except Discussion.DoesNotExist:
            discussion = None    
        self.assertIsNone(discussion)
        # Then check if the book has been created
        response = self.client.get(reverse('discussion_list'))
        self.assertQuerysetEqual(response.context['discussions'].all(),[])
        self.client.logout()

    def test_deletion_no_right(self):
        self.client.login(username='bub', password='bub')
        discussion = Discussion.objects.create(title='La vie et le reste')
        response = self.client.post(reverse('discussion_delete',args=[discussion.id]),{})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sharing/login/?next=' + reverse('discussion_delete',args=[discussion.id]))
        self.client.logout()

    def test_update(self):
        self.client.login(username='bob', password='bob')
        discussion = Discussion.objects.create(title='La vie et le reste')
        data = {
            'title': 'Les etoiles',
        }
       
        response = self.client.post(reverse('discussion_edit',args=[discussion.id]),data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('discussion_list'))
        try:
            discussion = Discussion.objects.get(**data)
        except Discussion.DoesNotExist:
            discussion = None    
        self.assertIsNotNone(discussion)
        self.client.logout()

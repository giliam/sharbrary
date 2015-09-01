# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

from utils.tests.common_test_case import CommonTestCase

from discussion.models import Discussion, Message

class DiscussionTestCase(CommonTestCase):
    def test_creation(self):
        self.client.login(username='bob', password='bob')
        data = {
            'title': 'Sujet de conversation',
        }

        response = self.client.post(reverse('discussion_new'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('discussion_detail',args=[1]))

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


class MessageTestCase(CommonTestCase):
    def setUp(self):
        super(MessageTestCase,self).setUp()
        self.client.login(username='bib', password='bib')
        self.discussion = Discussion.objects.create(title='La vie et le reste')

    def test_creation(self):
        self.client.login(username='bob', password='bob')
        data = {
            'message': 'Lorem ipsum lala bobium rasam est nivudae.',
        }

        response = self.client.post(reverse('message_new',args=[self.discussion.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('discussion_detail',args=[self.discussion.id]))

        try:
            message = Message.objects.get(discussion=self.discussion,**data)
        except Message.DoesNotExist:
            message = None    
        self.assertIsNotNone(message)
        # Then check if the book has been created
        response = self.client.get(reverse('discussion_detail',args=[self.discussion.id]))
        self.assertQuerysetEqual(response.context['messages_discussion'].all(),[repr(message)])
        self.client.logout()

    def test_creation_no_right(self):
        self.client.login(username='bub', password='bub')
        response = self.client.post(reverse('message_new',args=[self.discussion.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sharing/login/?next=' + reverse('message_new',args=[self.discussion.id]))
        self.client.logout()

    def test_deletion(self):
        self.client.login(username='bob', password='bob')
        message = Message.objects.create(discussion=self.discussion,message='Les pommes de terre sont cuites.')
        
        response = self.client.get(reverse('discussion_detail',args=[self.discussion.id]))
        self.assertQuerysetEqual(response.context['messages_discussion'].all(),[repr(message)])
        
        response = self.client.post(reverse('message_delete',args=[message.id]),{})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('discussion_list'))
        try:
            message = Message.objects.get(discussion=self.discussion,message="Les pommes de terre sont cuites.")
        except Message.DoesNotExist:
            message = None    
        self.assertIsNone(message)
        # Then check if the book has been created
        response = self.client.get(reverse('discussion_detail',args=[self.discussion.id]))
        self.assertQuerysetEqual(response.context['messages_discussion'].all(),[])
        self.client.logout()

    def test_deletion_no_right(self):
        self.client.login(username='bub', password='bub')
        message = Message.objects.create(discussion=self.discussion,message='Tout va bien ici !')
        response = self.client.post(reverse('message_delete',args=[message.id]),{})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sharing/login/?next=' + reverse('message_delete',args=[message.id]))
        self.client.logout()

    def test_deletion_not_my_message(self):
        self.client.login(username='bib', password='bib')
        message = Message.objects.create(discussion=self.discussion,message='Yoplait !',author=self.bob)
        response = self.client.post(reverse('message_delete',args=[message.id]),{})
        # only moderators can delete messages
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_update(self):
        self.client.login(username='bib', password='bib')
        message = Message.objects.create(discussion=self.discussion,message='La vie et le reste',author=self.bib)
        data = {
            'message': 'Les etoiles',
        }
       
        response = self.client.post(reverse('message_edit',args=[message.id]),data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('discussion_list'))
        try:
            message = Message.objects.get(**data)
        except Message.DoesNotExist:
            message = None    
        self.assertIsNotNone(message)
        self.client.logout()

    def test_update_not_my_message(self):
        self.client.login(username='bib', password='bib')
        message = Message.objects.create(discussion=self.discussion,message='Yoplait !',author=self.bob)
        data = {
            'message': 'Salut les amis, ça ne passera jamais de toute façon...',
        }
       
        response = self.client.post(reverse('message_edit',args=[message.id]),data)
        self.assertEqual(response.status_code, 403)
        try:
            message = Message.objects.get(discussion=self.discussion,**data)
        except Message.DoesNotExist:
            message = None    
        self.assertIsNone(message)
        self.client.logout()

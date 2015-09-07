# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

from utils.tests.common_test_case import CommonTestCase, with_login_user

from discussion.models import Discussion, Message

class DiscussionTestCase(CommonTestCase):
    @with_login_user()
    def test_creation(self):
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

    @with_login_user('bub')
    def test_creation_no_right(self):
        response = self.client.post(reverse('discussion_new'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sharing/login/?next=/discussion/discussion/new')

    @with_login_user()
    def test_deletion(self):
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

    @with_login_user('bub')
    def test_deletion_no_right(self):
        discussion = Discussion.objects.create(title='La vie et le reste')
        response = self.client.post(reverse('discussion_delete',args=[discussion.id]),{})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sharing/login/?next=' + reverse('discussion_delete',args=[discussion.id]))

    @with_login_user()
    def test_update(self):
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


class MessageTestCase(CommonTestCase):
    def setUp(self):
        super(MessageTestCase,self).setUp()
        self.discussion = Discussion.objects.create(title='La vie et le reste',author=self.bib)

    @with_login_user()
    def test_creation(self):
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

    @with_login_user('bub')
    def test_creation_no_right(self):
        response = self.client.post(reverse('message_new',args=[self.discussion.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sharing/login/?next=' + reverse('message_new',args=[self.discussion.id]))

    @with_login_user()
    def test_deletion(self):
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
    
    @with_login_user('bub')
    def test_deletion_no_right(self):
        message = Message.objects.create(discussion=self.discussion,message='Tout va bien ici !')
        response = self.client.post(reverse('message_delete',args=[message.id]),{})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/sharing/login/?next=' + reverse('message_delete',args=[message.id]))

    @with_login_user('bib')
    def test_deletion_not_my_message(self):
        message = Message.objects.create(discussion=self.discussion,message='Yoplait !',author=self.bob)
        response = self.client.post(reverse('message_delete',args=[message.id]),{})
        # only moderators can delete messages
        self.assertEqual(response.status_code, 403)

    @with_login_user('bib')
    def test_update(self):
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

    @with_login_user('bib')
    def test_update_not_my_message(self):
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

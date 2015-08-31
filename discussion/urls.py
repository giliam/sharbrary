# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from discussion import views

urlpatterns = patterns('',
  url(r'^$', permission_required('discussion.discussion_list')(views.DiscussionList.as_view()), name='discussion_list'),
  url(r'^discussion/$', permission_required('discussion.discussion_list')(views.DiscussionList.as_view()), name='discussion_list'),
  url(r'^discussion/(?P<discussion_id>\d+)$', permission_required('discussion.discussion_detail')(views.discussion_detail), name='discussion_detail'),
  url(r'^discussion/new$', permission_required('discussion.discussion_new')(views.DiscussionCreate.as_view()), name='discussion_new'),
  url(r'^discussion/edit/(?P<pk>\d+)$', permission_required('discussion.discussion_edit')(views.DiscussionUpdate.as_view()), name='discussion_edit'),
  url(r'^discussion/delete/(?P<pk>\d+)$', permission_required('discussion.discussion_delete')(views.DiscussionDelete.as_view()), name='discussion_delete'),

  url(r'^message/new/(?P<discussion_id>\d+)$', permission_required('discussion.message_new')(views.MessageCreate.as_view()), name='message_new'),
  url(r'^message/edit/(?P<pk>\d+)$', permission_required('discussion.message_edit')(views.MessageUpdate.as_view()), name='message_edit'),
  url(r'^message/delete/(?P<pk>\d+)$', permission_required('discussion.message_delete')(views.MessageDelete.as_view()), name='message_delete'),
)

# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from discussion import views

urlpatterns = patterns('',
  url(r'^$', permission_required('library.discussion_list')(views.DiscussionList.as_view()), name='discussion_list'),
  url(r'^discussion/$', permission_required('library.discussion_list')(views.DiscussionList.as_view()), name='discussion_list'),
  url(r'^discussion/(?P<discussion_id>\d+)$', permission_required('library.discussion_detail')(views.discussion_detail), name='discussion_detail'),
  url(r'^discussion/new$', permission_required('library.discussion_new')(views.DiscussionCreate.as_view()), name='discussion_new'),
  url(r'^discussion/edit/(?P<pk>\d+)$', permission_required('library.discussion_edit')(views.DiscussionUpdate.as_view()), name='discussion_edit'),
  url(r'^discussion/delete/(?P<pk>\d+)$', permission_required('library.discussion_delete')(views.DiscussionDelete.as_view()), name='discussion_delete'),
)

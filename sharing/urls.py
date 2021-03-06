# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import TemplateView 
from django.contrib.auth import views as auth_views

from sharing import views

urlpatterns = patterns('',
  url(r'^$', permission_required('sharing.lending_list')(views.LendingOnGoingList.as_view()), name='lending_list'),
  url(r'^lending/all$', permission_required('sharing.lending_list')(views.LendingAllList.as_view()), name='lending_list_all'),
  url(r'^lending/new$', permission_required('sharing.lending_new')(views.LendingCreate.as_view()), name='lending_new'),
  url(r'^lending/edit/(?P<pk>\d+)$', permission_required('sharing.lending_edit')(views.LendingUpdate.as_view()), name='lending_edit'),
  url(r'^lending/delete/(?P<pk>\d+)$', permission_required('sharing.lending_delete')(views.LendingDelete.as_view()), name='lending_delete'),
  url(r'^lending/end/(?P<lending_id>\d+)$', permission_required('sharing.lending_edit')(views.lending_end), name='lending_end'),

  url(r'^new/member$', permission_required('add_user')(views.member_add), name='member_add'),
  
  url(r'^borrowers/$', permission_required('sharing.borrower_list')(views.BorrowerList.as_view()), name='borrower_list'),

  url(r'^edit/profile/$', permission_required('sharing.profile_edit')(views.profile_edit), name='profile_edit'),
  url(r'^profile/show/(?P<profile_id>\d+)$', permission_required('sharing.profile_show')(views.profile_show), name='profile_show'),
  url(r'^dashboard/$', login_required(views.my_dashboard), name='dashboard'),
  
  url(r'^lend/book/(?P<book_id>\d+)$', permission_required('sharing.lending_new')(views.LendingBookCreate.as_view()), name='lend_book'),
  url(r'^borrow/a/book/$', permission_required('sharing.lending_new')(views.BorrowingCreate.as_view()), name='borrowing_create'),
  url(r'^borrow/this/copy/(?P<copy_id>\d+)$', permission_required('sharing.lending_new')(views.BorrowingCopyCreate.as_view()), name='borrowing_this_copy_create'),
  url(r'^borrow/this/book/(?P<book_id>\d+)$', permission_required('sharing.lending_new')(views.BorrowingBookCreate.as_view()), name='borrowing_this_book_create'),


  url(r'^queue/$', permission_required('sharing.queue_list')(views.QueueList.as_view()), name='queue_list'),
  url(r'^queue/new/$', permission_required('sharing.queue_new')(views.QueueCreate.as_view()), name='queue_new'),
  url(r'^queue/new/(?P<ownership_id>\d+)$', permission_required('sharing.queue_new')(views.QueueToBookCreate.as_view()), name='queue_new_book'),
  url(r'^queue/edit/(?P<pk>\d+)$', permission_required('sharing.queue_edit')(views.QueueUpdate.as_view()), name='queue_edit'),
  url(r'^queue/delete/(?P<pk>\d+)$', permission_required('sharing.queue_delete')(views.QueueDelete.as_view()), name='queue_delete'),


  url(r'^login/$', views.log_in, name='login'),
  url(r'^logout/$', views.log_out, name='logout'),
  url(r'^password_reset/$', auth_views.password_reset,{'template_name': 'base/password_reset.html'}, name='password_reset'),
  url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,{'template_name': 'base/password_reset.html'}, name='password_reset_confirm'),
  url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'base/password_reset_done.html'}, name='password_reset_done'),
  url(r'^password_reset/complete/$', auth_views.password_reset_complete,{'template_name': 'base/password_reset_complete.html'}, name='password_reset_complete'),
)
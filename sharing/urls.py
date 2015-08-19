# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import TemplateView 

from sharing import views

urlpatterns = patterns('',
  url(r'^$', permission_required('sharing.lending_list')(views.LendingOnGoingList.as_view()), name='lending_list'),
  url(r'^lending/all$', permission_required('sharing.lending_list')(views.LendingAllList.as_view()), name='lending_list_all'),
  url(r'^lending/new$', permission_required('sharing.lending_new')(views.LendingCreate.as_view()), name='lending_new'),
  url(r'^lending/edit/(?P<pk>\d+)$', permission_required('sharing.lending_edit')(views.LendingUpdate.as_view()), name='lending_edit'),
  url(r'^lending/delete/(?P<pk>\d+)$', permission_required('sharing.lending_delete')(views.LendingDelete.as_view()), name='lending_delete'),
  url(r'^lending/end/(?P<lending_id>\d+)$', permission_required('sharing.lending_end')(views.lending_end), name='lending_end'),

  url(r'^new/member$', permission_required('add_user')(views.member_add), name='member_add'),
  
  url(r'^borrowers/$', permission_required('sharing.borrower_list')(views.BorrowerList.as_view()), name='borrower_list'),
  url(r'^profile/show/(?P<profile_id>\d+)$', permission_required('sharing.profile_show')(views.profile_show), name='profile_show'),
  url(r'^dashboard/$', login_required(views.my_dashboard), name='dashboard'),
  
  url(r'^lend/book/(?P<book_id>\d+)$', permission_required('sharing.lending_new')(views.LendingBookCreate.as_view()), name='lend_book'),
  url(r'^borrow/a/book/$', permission_required('sharing.lending_new')(views.BorrowingCreate.as_view()), name='borrowing_create'),
  url(r'^borrow/this/book/(?P<book_id>\d+)$', permission_required('sharing.lending_new')(views.BorrowingBookCreate.as_view()), name='borrowing_this_book_create'),

  url(r'^login/$', views.log_in, name='login'),
  url(r'^logout/$', views.log_out, name='logout'),
)
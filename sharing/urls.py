from django.conf.urls import patterns, url

from sharing import views

urlpatterns = patterns('',
  url(r'^$', views.LendingList.as_view(), name='lending_list'),
  url(r'^lending/new$', views.LendingCreate.as_view(), name='lending_new'),
  url(r'^lending/edit/(?P<pk>\d+)$', views.LendingUpdate.as_view(), name='lending_edit'),
  url(r'^lending/delete/(?P<pk>\d+)$', views.LendingDelete.as_view(), name='lending_delete'),
  url(r'^borrowers/$', views.BorrowerList.as_view(), name='borrower_list'),
)
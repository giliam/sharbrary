from django.conf.urls import patterns, url

from sharing import views

urlpatterns = patterns('',
  url(r'^$', views.LendingList.as_view(), name='lending_list'),
  url(r'^lending/new$', views.LendingCreate.as_view(), name='lending_new'),
  url(r'^lending/edit/(?P<pk>\d+)$', views.LendingUpdate.as_view(), name='lending_edit'),
  url(r'^lending/delete/(?P<pk>\d+)$', views.LendingDelete.as_view(), name='lending_delete'),
  url(r'^lending/end/(?P<lending_id>\d+)$', 'sharing.views.end_lending', name='lending_end'),
  url(r'^borrowers/$', views.BorrowerList.as_view(), name='borrower_list'),
  url(r'^login/$', views.log_in, name='login'),
  url(r'^logout/$', views.log_out, name='logout'),
)
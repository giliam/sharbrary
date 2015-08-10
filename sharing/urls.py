from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from sharing import views

urlpatterns = patterns('',
  url(r'^$', permission_required('sharing.lending_list')(views.LendingOnGoingList.as_view()), name='lending_list'),
  url(r'^lending/new$', permission_required('sharing.lending_new')(views.LendingCreate.as_view()), name='lending_new'),
  url(r'^lending/edit/(?P<pk>\d+)$', permission_required('sharing.lending_edit')(views.LendingUpdate.as_view()), name='lending_edit'),
  url(r'^lending/delete/(?P<pk>\d+)$', permission_required('sharing.lending_delete')(views.LendingDelete.as_view()), name='lending_delete'),
  url(r'^lending/end/(?P<lending_id>\d+)$', permission_required('sharing.lending_end')(views.lending_end), name='lending_end'),
  url(r'^borrowers/$', permission_required('sharing.borrower_list')(views.BorrowerList.as_view()), name='borrower_list'),
  url(r'^login/$', views.log_in, name='login'),
  url(r'^logout/$', views.log_out, name='logout'),
)
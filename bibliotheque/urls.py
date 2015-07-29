from django.conf.urls import patterns, url

from bibliotheque import views

urlpatterns = patterns('',
  url(r'^$', views.LivreList.as_view(), name='livre_liste'),
  url(r'^ajoute$', views.LivreCreate.as_view(), name='livre_ajoute'),
  url(r'^modifie/(?P<pk>\d+)$', views.LivreUpdate.as_view(), name='livre_modifie'),
  url(r'^supprime/(?P<pk>\d+)$', views.LivreDelete.as_view(), name='livre_supprime'),
)
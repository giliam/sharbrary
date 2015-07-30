from django.conf.urls import patterns, url

from library import views

urlpatterns = patterns('',
  url(r'^$', views.BookList.as_view(), name='book_list'),
  url(r'^new$', views.BookCreate.as_view(), name='book_new'),
  url(r'^edit/(?P<pk>\d+)$', views.BookUpdate.as_view(), name='book_edit'),
  url(r'^delete/(?P<pk>\d+)$', views.BookDelete.as_view(), name='book_delete'),
  url(r'author/^$', views.AuthorList.as_view(), name='author_list'),
  url(r'^author/new$', views.AuthorCreate.as_view(), name='author_new'),
  url(r'^author/edit/(?P<pk>\d+)$', views.AuthorUpdate.as_view(), name='author_edit'),
  url(r'^author/delete/(?P<pk>\d+)$', views.AuthorDelete.as_view(), name='author_delete'),
)
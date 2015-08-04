from django.conf.urls import patterns, url

from library import views

urlpatterns = patterns('',
  url(r'^$', views.BookList.as_view(), name='book_list'),
  url(r'^book/new$', views.BookCreate.as_view(), name='book_new'),
  url(r'^book/edit/(?P<pk>\d+)$', views.BookUpdate.as_view(), name='book_edit'),
  url(r'^book/delete/(?P<pk>\d+)$', views.BookDelete.as_view(), name='book_delete'),
  url(r'^author/$', views.AuthorList.as_view(), name='author_list'),
  url(r'^author/new$', views.AuthorCreate.as_view(), name='author_new'),
  url(r'^author/edit/(?P<pk>\d+)$', views.AuthorUpdate.as_view(), name='author_edit'),
  url(r'^author/delete/(?P<pk>\d+)$', views.AuthorDelete.as_view(), name='author_delete'),
  url(r'^editor/$', views.EditorList.as_view(), name='editor_list'),
  url(r'^editor/new$', views.EditorCreate.as_view(), name='editor_new'),
  url(r'^editor/edit/(?P<pk>\d+)$', views.EditorUpdate.as_view(), name='editor_edit'),
  url(r'^editor/delete/(?P<pk>\d+)$', views.EditorDelete.as_view(), name='editor_delete'),
  url(r'^theme/$', views.ThemeList.as_view(), name='theme_list'),
  url(r'^theme/new$', views.ThemeCreate.as_view(), name='theme_new'),
  url(r'^theme/edit/(?P<pk>\d+)$', views.ThemeUpdate.as_view(), name='theme_edit'),
  url(r'^theme/delete/(?P<pk>\d+)$', views.ThemeDelete.as_view(), name='theme_delete'),
)
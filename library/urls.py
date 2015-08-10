from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from library import views

urlpatterns = patterns('',
  url(r'^$', permission_required('library.book_list')(views.BookList.as_view()), name='book_list'),
  url(r'^book/new$', permission_required('library.book_new')(views.BookCreate.as_view()), name='book_new'),
  url(r'^book/edit/(?P<pk>\d+)$', permission_required('library.book_edit')(views.BookUpdate.as_view()), name='book_edit'),
  url(r'^book/delete/(?P<pk>\d+)$', permission_required('library.book_delete')(views.BookDelete.as_view()), name='book_delete'),
  url(r'^author/$', permission_required('library.author_list')(views.AuthorList.as_view()), name='author_list'),
  url(r'^author/new$', permission_required('library.author_new')(views.AuthorCreate.as_view()), name='author_new'),
  url(r'^author/edit/(?P<pk>\d+)$', permission_required('library.author_edit')(views.AuthorUpdate.as_view()), name='author_edit'),
  url(r'^author/delete/(?P<pk>\d+)$', permission_required('library.author_delete')(views.AuthorDelete.as_view()), name='author_delete'),
  url(r'^editor/$', permission_required('library.editor_list')(views.EditorList.as_view()), name='editor_list'),
  url(r'^editor/new$', permission_required('library.editor_new')(views.EditorCreate.as_view()), name='editor_new'),
  url(r'^editor/edit/(?P<pk>\d+)$', permission_required('library.editor_edit')(views.EditorUpdate.as_view()), name='editor_edit'),
  url(r'^editor/delete/(?P<pk>\d+)$', permission_required('library.editor_delete')(views.EditorDelete.as_view()), name='editor_delete'),
  url(r'^theme/$', permission_required('library.theme_list')(views.ThemeList.as_view()), name='theme_list'),
  url(r'^theme/new$', permission_required('library.theme_new')(views.ThemeCreate.as_view()), name='theme_new'),
  url(r'^theme/edit/(?P<pk>\d+)$', permission_required('library.theme_edit')(views.ThemeUpdate.as_view()), name='theme_edit'),
  url(r'^theme/delete/(?P<pk>\d+)$', permission_required('library.theme_delete')(views.ThemeDelete.as_view()), name='theme_delete'),
)
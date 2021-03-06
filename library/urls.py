# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from library import views

urlpatterns = patterns('',
  url(r'^$', permission_required('library.book_list')(views.BookList.as_view()), name='book_list'),
  url(r'^book/new$', permission_required('library.book_new')(views.BookCreate.as_view()), name='book_new'),
  url(r'^book/add/to/my/library$', permission_required('library.book_new')(views.OwnershipCreate.as_view()), name='book_add_to_my_library'),
  url(r'^book/add/(?P<book_id>\d+)/my/library$', permission_required('library.book_new')(views.BookOwnershipCreate.as_view()), name='book_add_this_to_my_library'),
  url(r'^book/detail/(?P<book_id>\d+)$', permission_required('library.book_detail')(views.book_detail), name='book_detail'),
  url(r'^book/edit/(?P<pk>\d+)$', permission_required('library.book_edit')(views.BookUpdate.as_view()), name='book_edit'),
  url(r'^book/delete/(?P<pk>\d+)$', permission_required('library.book_delete')(views.BookDelete.as_view()), name='book_delete'),
  url(r'^book/remove/from/library/(?P<book_id>\d+)$', permission_required('library.book_remove_from_library')(views.book_remove_from_library), name='book_remove_from_library'),
  url(r'^book/rate/(?P<book_id>\d+)/(?P<value>\d+)/$', permission_required('library.book_rate')(views.book_rate), name='book_rate'),

  url(r'^box/book/new$', permission_required('library.book_box_new')(views.BookCreate.as_view()), {'on_shelf':False}, name='book_box_new'),
  url(r'^box$', permission_required('library.book_box_list')(views.BoxList.as_view()), {'on_shelf':False}, name='book_box_list'),


  url(r'^ownership/edit/(?P<pk>\d+)$', permission_required('library.owernship_edit')(views.OwnershipUpdate.as_view()), name='ownership_edit'),
  url(r'^ownership/delete/(?P<pk>\d+)$', permission_required('library.owernship_delete')(views.OwnershipDelete.as_view()), name='ownership_delete'),

  url(r'^research/$', permission_required('library.book_list')(views.book_research), name='book_research'),

  url(r'^homepage/edit/$', permission_required('library.page_edit')(views.homepage_edit), {'page_name':'homepage'}, name='homepage_edit'),
  url(r'^header/edit/$', permission_required('library.page_edit')(views.homepage_edit), {'page_name':'header_title'}, name='header_edit'),
 
  url(r'^author/$', permission_required('library.author_list')(views.AuthorList.as_view()), name='author_list'),
  url(r'^author/detail/(?P<author_id>\d+)$', permission_required('library.author_detail')(views.author_detail), name='author_detail'),
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
 
  url(r'^period/$', permission_required('library.period_list')(views.PeriodList.as_view()), name='period_list'),
  url(r'^period/new$', permission_required('library.period_new')(views.PeriodCreate.as_view()), name='period_new'),
  url(r'^period/edit/(?P<pk>\d+)$', permission_required('library.period_edit')(views.PeriodUpdate.as_view()), name='period_edit'),
  url(r'^period/delete/(?P<pk>\d+)$', permission_required('library.period_delete')(views.PeriodDelete.as_view()), name='period_delete'),
)

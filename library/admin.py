# coding: utf-8
from django.contrib import admin
from library.models import Author, Editor, Theme, Book

admin.site.register(Author)
admin.site.register(Editor)
admin.site.register(Theme)
admin.site.register(Book)
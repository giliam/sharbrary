from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from library.models import Book, Author, Editor, Theme

class BookList(ListView):
    model = Book
    template_name="library/book_list.html"

class BookCreate(CreateView):
    model = Book
    success_url = reverse_lazy('book_list')
    fields = ['title', 'publishing_date', 'author', 'themes', 'summary']

class BookUpdate(UpdateView):
    model = Book
    success_url = reverse_lazy('book_list')
    fields = ['title', 'publishing_date', 'author', 'themes', 'summary']

class BookDelete(DeleteView):
    model = Book
    template_name="library/book_confirm_delete.html"
    success_url = reverse_lazy('book_list')

class AuthorList(ListView):
    model = Author
    template_name="library/author_list.html"

class AuthorCreate(CreateView):
    model = Author
    success_url = reverse_lazy('author_list')
    fields = ['firstname', 'lastname', 'birthdate', 'death_date']

class AuthorUpdate(UpdateView):
    model = Author
    success_url = reverse_lazy('author_list')
    fields = ['firstname', 'lastname', 'birthdate', 'death_date']

class AuthorDelete(DeleteView):
    model = Author
    template_name="library/author_confirm_delete.html"
    success_url = reverse_lazy('author_list')

class EditorList(ListView):
    model = Editor
    template_name="library/editor_list.html"

class EditorCreate(CreateView):
    model = Editor
    success_url = reverse_lazy('editor_list')
    fields = ['name']

class EditorUpdate(UpdateView):
    model = Editor
    success_url = reverse_lazy('editor_list')
    fields = ['name']

class EditorDelete(DeleteView):
    model = Editor
    template_name="library/editor_confirm_delete.html"
    success_url = reverse_lazy('editor_list')

class ThemeList(ListView):
    model = Theme
    template_name="library/theme_list.html"

class ThemeCreate(CreateView):
    model = Theme
    success_url = reverse_lazy('theme_list')
    fields = ['name', 'period']

class ThemeUpdate(UpdateView):
    model = Theme
    success_url = reverse_lazy('theme_list')
    fields = ['name', 'period']

class ThemeDelete(DeleteView):
    model = Theme
    template_name="library/theme_confirm_delete.html"
    success_url = reverse_lazy('theme_list')
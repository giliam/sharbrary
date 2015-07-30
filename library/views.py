from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from library.models import Book, Author

class BookList(ListView):
    model = Book
    template_name="library/book_list.html"

class BookCreate(CreateView):
    model = Book
    success_url = reverse_lazy('book_list')
    fields = ['title', 'publishing_date', 'author']

class BookUpdate(UpdateView):
    model = Book
    success_url = reverse_lazy('book_list')
    fields = ['title', 'publishing_date', 'author']

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

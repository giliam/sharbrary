from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from library.models import Book

class BookList(ListView):
    model = Book
    template_name="library/book_liste.html"

class BookCreate(CreateView):
    model = Book
    success_url = reverse_lazy('book_liste')
    fields = ['titre', 'annee_parution']

class BookUpdate(UpdateView):
    model = Book
    success_url = reverse_lazy('book_liste')
    fields = ['titre', 'annee_parution']

class BookDelete(DeleteView):
    model = Book
    template_name="library/book_confirme_suppression.html"
    success_url = reverse_lazy('book_liste')

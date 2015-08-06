from django.shortcuts import render
from sharing.models import Lending

class BookList(ListView):
    model = Book
    template_name="sharing/book_list.html"

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
    template_name="sharing/book_confirm_delete.html"
    success_url = reverse_lazy('book_list')
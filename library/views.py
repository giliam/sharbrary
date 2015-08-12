from django.shortcuts import render
from django.views.generic import TemplateView,ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from library.models import Book, Author, Editor, Theme, Period
from sharing.models import Lending

from utils.models.sortmixin import SortMixin

def book_detail(request, book_id):
    """
    Shows book details.
    """
    book = get_object_or_404(Book, pk=book_id)
    lendings = Lending.objects.filter(book__id=book_id)
    return render(request, 'library/book_detail.html', {'book':book,'lendings':lendings})

class BookEmbedList(SortMixin):
    context_object_name = "books"
    default_sort_params = ('title', 'asc')
    allowed_sort_params = ['title', 'author__lastname', 'editor__name', 'published', 'owner__username']
    model = Book
    template_name="library/book_embed_list.html"
    paginate_by = 20

class BookList(BookEmbedList):
    template_name="library/book_list.html"

class BookCreate(SuccessMessageMixin, CreateView):
    model = Book
    success_url = reverse_lazy('book_list')
    success_message = _("%(title)s was created successfully")
    fields = ['title', 'publishing_date', 'author', 'owner', 'themes', 'periods', 'summary', 'cover']

class BookUpdate(SuccessMessageMixin, UpdateView):
    model = Book
    success_url = reverse_lazy('book_list')
    success_message = _("%(title)s was updated successfully")
    fields = ['title', 'publishing_date', 'author', 'owner', 'themes', 'periods', 'summary', 'cover']

class BookDelete(DeleteView):
    model = Book
    template_name="library/book_confirm_delete.html"
    success_url = reverse_lazy('book_list')

def author_detail(request, author_id):
    """
    Shows author details.
    """
    sort_by = request.GET.get('sort_by', "title")
    order = request.GET.get('order', "asc")

    author = get_object_or_404(Author, pk=author_id)
    books = Book.objects.filter(author=author).order_by(sort_by)
    if order == 'desc':
        books = books.reverse()
    return render(request, 'library/author_detail.html', {'author':author,'books':books})

class AuthorList(SortMixin):
    context_object_name = "authors"
    default_sort_params = ('lastname', 'asc')
    allowed_sort_params = ['lastname', 'birthdate', 'death_date']
    model = Author
    template_name="library/author_list.html"
    paginate_by = 20

class AuthorCreate(SuccessMessageMixin, CreateView):
    model = Author
    success_url = reverse_lazy('author_list')
    success_message = _("The author %(firstname)s %(lastname)s was added successfully")
    fields = ['firstname', 'lastname', 'birthdate', 'death_date']

class AuthorUpdate(SuccessMessageMixin, UpdateView):
    model = Author
    success_url = reverse_lazy('author_list')
    success_message = _("%(firstname)s %(lastname)s was updated successfully")
    fields = ['firstname', 'lastname', 'birthdate', 'death_date']

class AuthorDelete(DeleteView):
    model = Author
    template_name="library/author_confirm_delete.html"
    success_url = reverse_lazy('author_list')

class EditorList(SortMixin):
    context_object_name = "editors"
    default_sort_params = ('name', 'asc')
    allowed_sort_params = ['name']
    model = Editor
    template_name="library/editor_list.html"
    paginate_by = 20

class EditorCreate(SuccessMessageMixin, CreateView):
    model = Editor
    success_url = reverse_lazy('editor_list')
    success_message = _("%(name)s was created successfully")
    fields = ['name']

class EditorUpdate(SuccessMessageMixin, UpdateView):
    model = Editor
    success_url = reverse_lazy('editor_list')
    success_message = _("%(name)s was updated successfully")
    fields = ['name']

class EditorDelete(DeleteView):
    model = Editor
    template_name="library/editor_confirm_delete.html"
    success_url = reverse_lazy('editor_list')

class ThemeList(SortMixin):
    context_object_name = "themes"
    default_sort_params = ('name', 'asc')
    allowed_sort_params = ['name']
    model = Theme
    template_name="library/theme_list.html"
    paginate_by = 20

class ThemeCreate(SuccessMessageMixin, CreateView):
    model = Theme
    success_url = reverse_lazy('theme_list')
    success_message = _("%(name)s was added successfully")
    fields = ['name']

class ThemeUpdate(SuccessMessageMixin, UpdateView):
    model = Theme
    success_url = reverse_lazy('theme_list')
    success_message = _("%(name)s was updated successfully")
    fields = ['name']

class ThemeDelete(DeleteView):
    model = Theme
    template_name="library/theme_confirm_delete.html"
    success_url = reverse_lazy('theme_list')

class PeriodList(SortMixin):
    context_object_name = "periods"
    default_sort_params = ('name', 'asc')
    allowed_sort_params = ['name']
    model = Period
    template_name="library/period_list.html"
    paginate_by = 20

class PeriodCreate(SuccessMessageMixin, CreateView):
    model = Period
    success_url = reverse_lazy('period_list')
    success_message = _("%(name)s was added successfully")
    fields = ['name']

class PeriodUpdate(SuccessMessageMixin, UpdateView):
    model = Period
    success_url = reverse_lazy('period_list')
    success_message = _("%(name)s was updated successfully")
    fields = ['name']

class PeriodDelete(DeleteView):
    model = Period
    template_name="library/period_confirm_delete.html"
    success_url = reverse_lazy('period_list')
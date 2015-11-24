# coding: utf-8
import json

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.db.models import Q

from library.models import Book, Page, Author, Editor, Theme, Period, Ownership, Opinion, OPINION_NOTATION_VALUES
from library.forms import SelectOwnerForm, ResearchForm, PageForm
from sharing.models import Lending, Queue
from discussion.models import Discussion

from utils.models.sortmixin import SortMixin
from utils.models.conditions import actual_lending, one_of_these_books
from utils.models.authorizations import CheckOwner

class HomePageView(TemplateView):
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        number_of_books = 3
        context = super(HomePageView, self).get_context_data(**kwargs)
        try:
            context['homepage_message'] = Page.objects.get(name='homepage')
        except Page.DoesNotExist:
            context['homepage_message'] = None
        context['latest_books'] = Book.objects.order_by('-added_date').all()[:number_of_books]
        context['best_books'] = Book.objects.raw('SELECT lb.*, AVG(COALESCE(lo.value,0)) AS value_avg FROM library_book AS lb LEFT JOIN library_opinion AS lo ON lo.book_id = lb.id GROUP BY lb.id ORDER BY value_avg DESC')[:number_of_books]
        return context


@permission_required('library.book_detail')
def book_detail(request, book_id):
    """
    Shows book details.
    """
    book = get_object_or_404(Book, pk=book_id, on_shelf=True)
    ownerships = Ownership.objects.filter(book__id=book_id)
    queues = Queue.objects.filter(book_copy__book__id=book_id,fulfilled=False).order_by('added_date')
    lendings = Lending.objects.filter(actual_lending(),book_copy__book__id=book_id)
    
    try:
        opinion = Opinion.objects.get(book__id=book_id,author=request.user)
        rating_user = opinion.value
    except Opinion.DoesNotExist:
        rating_user = None
    queues_ordered = {ownership.id:[] for ownership in ownerships}
    # copy is not enough here, because of lists probably
    lendings_ordered = {ownership.id:[] for ownership in ownerships}
    # group them by ownership id
    for queue in queues.all():
        queues_ordered[queue.book_copy.id].append(queue)
    for lending in lendings.all():
        lendings_ordered[lending.book_copy.id].append(lending)

    return render(request, 'library/book_detail.html', {'book':book,'lendings':lendings,'lendings_ordered':lendings_ordered,'queues_ordered':queues_ordered,'ownerships':ownerships,'rating_user':rating_user, 'opinion_notation_values':OPINION_NOTATION_VALUES})

class BookEmbedList(SortMixin):
    context_object_name = "books"
    default_sort_params = ('title', 'asc')
    allowed_sort_params = ['title', 'author__lastname', 'editor__name', 'publishing_date']
    model = Book
    template_name="library/book_embed_list.html"
    paginate_by = 20

    def get_queryset(self):
        return self.sort_queryset(Book.objects.filter(on_shelf=True))


class BookList(BookEmbedList):
    template_name="library/book_list.html"
    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        books_owned = Book.objects.raw("SELECT DISTINCT lb.id FROM library_book AS lb INNER JOIN library_ownership AS lo ON lo.book_id = lb.id")
        context['form'] = ResearchForm()
        context['books_owned'] = {book.id:True for book in books_owned}
        return context

class BoxList(BookEmbedList):
    template_name="library/box_list.html"
    paginate_by = 100
    def get_queryset(self):
        return self.sort_queryset(Book.objects.filter(on_shelf=False))

class BookCreate(CreateView):
    model = Book
    success_url = reverse_lazy('book_list')
    success_message = _("%(title)s was created successfully")
    fields = ['title', 'publishing_date', 'author', 'owners', 'themes', 'summary', 'cover']

    def form_valid(self, form):
        book = form.save(commit=False)
        book.on_shelf = self.kwargs.get('on_shelf',True)
        book.save()
        for owner in form.cleaned_data['owners']:
            ownership = Ownership()
            ownership.book = book
            ownership.owner = owner
            ownership.save()

        # Create a discussion onto forum.
        discussion = Discussion()
        if book.author:
            discussion.title = _("Discussion on %(book)s (%(author)s)") % {'author':book.author,'book':book.title}
        else:
            discussion.title = _("Discussion on %(book)s") % {'book':book.title}
        discussion.author = self.request.user
        discussion.save()

        messages.add_message(self.request, messages.SUCCESS, self.success_message % {'title':book.title})
        if book.on_shelf:
            return redirect('book_detail',book_id=book.id)
        else:
            return redirect('book_box_list')


class BookUpdate(UpdateView):
    model = Book
    success_url = reverse_lazy('book_list')
    success_message = _("%(title)s was updated successfully")
    fields = ['title', 'publishing_date', 'author', 'themes', 'periods', 'summary', 'cover']
    def form_valid(self, form):
        book = form.save()

        messages.add_message(self.request, messages.SUCCESS, self.success_message % {'title':book.title})
        if book.on_shelf:
            return redirect('book_detail',book_id=book.id)
        else:
            return redirect('book_box_list')

class BookDelete(DeleteView):
    model = Book
    template_name="library/book_confirm_delete.html"
    success_url = reverse_lazy('book_list')

@permission_required('library.book_remove_from_library')
def book_remove_from_my_library(request, book):
    """
    Removes a book from my own library.
    """
    if not request.user in book.owners.all():
        # Mistakenly arrived here.
        messages.add_message(request, messages.ERROR, _('This book is not in your library and you have no right to remove it from someone else library.'))
        return redirect('book_list')
    if request.method == 'POST':
        Ownership.objects.filter(owner__id=request.user.id).clear()
        messages.add_message(request, messages.SUCCESS, _('The book has been successfully removed from your library.'))
        return redirect('book_list')
    return None

@permission_required('library.book_remove_from_library')
def book_remove_from_library(request, book_id):
    """
    Removes a book from someone's library.
    """
    # First get the book.
    book = get_object_or_404(Book, pk=book_id, on_shelf=True)
    
    # If not owners at all, no need to remove anyone
    if not book.owners.all(): 
        raise Http404
    # If can remove from all libraries, then display the form with all current owners.
    if request.user.has_perm('library.book_remove_from_all_libraries'):
        if request.method == 'POST':
            # Creates a form hydrated with current owners of book.
            this_book_ownerships = Ownership.objects.filter(book__id=book_id).all()
            form = SelectOwnerForm(request.POST,owners=this_book_ownerships)
            if form.is_valid():
                # Makes a list of all ownership on this book.
                authorized_ids = [ownership.id for ownership in this_book_ownerships]

                # Then applies the modifications
                for ownership in form.cleaned_data['owners']:
                    # If the ownership concerns this book
                    if ownership.id in authorized_ids:
                        ownership.delete()
                
                messages.add_message(request, messages.SUCCESS, _('The book has been successfully removed from the library of %(owners)s.') % {'owners':', '.join([owner.owner.username for owner in form.cleaned_data['owners']])})
                return redirect('book_list')
        else:
            form = SelectOwnerForm(owners=Ownership.objects.filter(book__id=book_id).all())        
        messages.add_message(request, messages.WARNING, _('You are going to remove the book from someone\'s library.'))
        return render(request, 'library/book_remove_from_library.html', {'object':book,'form':form})
    else:
        # Has no permission so calls remove from my own library function which only implements a confirmation.
        response = book_remove_from_my_library(request,book)
        if response:
            return response
    return render(request, 'library/book_confirm_delete.html', {'object':book})

def determine_new_ownership_necessary(new_ownership,existing_ownership):
    """
    Determine wether a new ownership should be created or if an existing ownership can be updated.
    Cases that create a new ownership:
        * no existing ownership
        * an existing ownership with a different editor than the new one
        * an existing ownership without editor
        * an existing ownership with a different cover
    """
    # We only edit the ownership from the same owner.
    if existing_ownership and existing_ownership.owner == new_ownership.owner:
        # an existing ownership with a different editor than the new one
        if existing_ownership.editor and new_ownership.editor and new_ownership.editor != existing_ownership.editor:
            return True
        # an existing ownership without editor
        if existing_ownership.editor and not new_ownership.editor:
            return True
        # an existing ownership with a different cover
        if new_ownership.cover and existing_ownership.cover and new_ownership.cover != existing_ownership.cover:            
            return True
        return False
    else:
        return True

def add_book_to_library(request,ownership):
    """
    Manages to add a book to someone's library.
    """
    existing_ownerships = Ownership.objects.filter(book__id=ownership.book.id,owner__id=request.user.id)
    # If we are editing an existing ownership.
    if ownership.id:
        existing_ownerships = existing_ownerships.exclude(id=ownership.id)
    
    should_save_this_one = True
    for existing_ownership in existing_ownerships.all():
        # If there is an ownership that corresponds to this one, than we have to edit it.
        if not determine_new_ownership_necessary(ownership,existing_ownership):
            should_save_this_one = False
            break
    # If we should create a new one or at least edit the one existing
    if should_save_this_one:
        ownership.owner = request.user
        ownership.save()
        return True
    # Else, we update the existing ownership that matches our inputs.
    else:
        modified_fields = []
        # Adds copies and gets which fieldswere modified
        existing_ownership.copies += ownership.copies
        modified_fields.append(_("copies"))
        if not existing_ownership.comments and ownership.comments:
            existing_ownership.comments = ownership.comments
            modified_fields.append(_("comments"))
        if not existing_ownership.editor and ownership.editor:
            existing_ownership.editor = ownership.editor
            modified_fields.append(_("editor"))
        if not existing_ownership.cover and ownership.cover:
            existing_ownership.cover = ownership.cover
            modified_fields.append(_("cover"))
        messages.add_message(request, messages.WARNING, _('You already had this book in your library so your previous ownership was updated. More precisely, these fields - %(fields)s - where updated.') % {'fields':(', '.join(str(s) for s in modified_fields))})
        existing_ownership.save()
        return False

def update_book_of_library(request,ownership):
    """
    Manages to update a book to someone's library.
    """
    # If an existing ownership was created, then you can remove this one.
    if not add_book_to_library(request,ownership):
        ownership.delete()

class OwnershipCreate(SuccessMessageMixin, CreateView):
    model = Ownership
    success_url = reverse_lazy('book_list')
    success_message = _("%(book)s was added successfully to your library")
    fields = ['book', 'copies', 'editor', 'comments', 'cover']
    def form_valid(self, form):
        ownership = form.save(commit=False)    
        if not ownership.book.on_shelf:
            raise Http404(_("Book does not exist on the shelf! (maybe in the box?)"))
        add_book_to_library(self.request,ownership)
        return redirect('book_detail',book_id=ownership.book.id)

class OwnershipUpdate(SuccessMessageMixin, UpdateView, CheckOwner):
    model = Ownership
    success_url = reverse_lazy('book_list')
    success_message = _("%(book)s from your library was modified successfully.")
    fields = ['copies', 'editor', 'comments', 'cover']
    owner_field = 'owner'
    def form_valid(self, form):
        ownership = form.save(commit=False)
        ownership.book = self.get_object().book
        update_book_of_library(self.request,ownership)
        return redirect('book_detail',book_id=ownership.book.id)

class OwnershipDelete(SuccessMessageMixin, DeleteView, CheckOwner):
    model = Ownership
    success_url = reverse_lazy('book_list')
    success_message = _("%(book)s was deleted successfully from your library")
    owner_field = 'owner'

class BookOwnershipCreate(OwnershipCreate):
    fields = ['copies', 'editor', 'comments', 'cover']
    def form_valid(self, form):
        ownership = form.save(commit=False)
        ownership.owner = self.request.user
        ownership.book = get_object_or_404(Book,pk=self.kwargs['book_id'], on_shelf=True)
        add_book_to_library(self.request,ownership)
        return redirect('book_detail',book_id=ownership.book.id)


def author_detail(request, author_id):
    """
    Shows author details.
    """
    sort_by = request.GET.get('sort_by', "title")
    order = request.GET.get('order', "asc")

    author = get_object_or_404(Author, pk=author_id)
    books = Book.objects.filter(author=author, on_shelf=True).order_by(sort_by)
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


@permission_required('library.book_list')
def book_research(request):
    """
    Looks for something in the library
    """
    sort_by = request.GET.get('sort_by', "title")
    order = request.GET.get('order', "asc")
    ResearchForm
    if request.method == 'POST':
        form = ResearchForm(request.POST)
        if form.is_valid():
            research = form.cleaned_data['research']
            books = Book.objects.filter(Q(title__icontains=research)|Q(editor__name__icontains=research)|Q(author__firstname__icontains=research)|Q(author__lastname__icontains=research)|Q(summary__icontains=research)).order_by(sort_by)
        else:
            messages.add_message(request, messages.ERROR, _('The research was not successfully done.'))
            books = Book.objects.all()
    else:
        form = ResearchForm()
        books = Book.objects.all()
    if order == 'desc':
        books = books.reverse()
    return render(request, 'library/book_list.html', {'form':form,'books':books})

@permission_required('library.book_rate')
def book_rate(request, book_id, value):
    """
    Sets the notation of a book for a specific user.
    """
    value = int(value)
    book = get_object_or_404(Book, pk=book_id, on_shelf=True)
    if value not in range(0,6):
        raise Exception, _("Value not available !")

    try:
        opinion = Opinion.objects.get(book=book,author=request.user)
    except Opinion.DoesNotExist:
        opinion = Opinion()
        opinion.book = book
        opinion.author = request.user
    opinion.value = value
    opinion.save()
    return HttpResponse(json.dumps({"value":value}),content_type="application/json")

@permission_required('library.page_edit')
def homepage_edit(request,page_name="homepage"):
    """
    Edit the home page
    """
    try:
        homepage = Page.objects.get(name=page_name)
    except Page.DoesNotExist:
        homepage = Page()
        homepage.name = page_name

    if request.method == "POST":
        form_homepage = PageForm(request.POST,instance=homepage)
        if form_homepage.is_valid():
            form_homepage.save()
            messages.add_message(request, messages.SUCCESS, _("The page has been successfully edited!"))
            form_homepage = PageForm(instance=homepage)
    else:
        form_homepage = PageForm(instance=homepage)
    return render(request, 'library/page_form.html', {'form':form_homepage})
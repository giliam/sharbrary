# coding: utf-8
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.translation import ugettext_lazy as _, activate as translation_activate, LANGUAGE_SESSION_KEY
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

from sharing.models import Lending, Profile, Queue
from sharing.forms import LendingEndForm, LogInForm, LendingForm, ProfileForm, UserForm,UserEditForm
from library.models import Book, Ownership

from utils.models.sortmixin import SortMixin
from utils.models.conditions import actual_lending
from utils.models.availability import is_lending_possible, is_queueing_possible

def remove_from_queue(book_copy,borrower,lending=None):
    queues = Queue.objects.filter(book_copy=book_copy,borrower=borrower,fulfilled=0)
    for queue in queues.all():
        queue.fulfilled = 1
        if lending:
            queue.lending = lending
        queue.save()

class LendingAllList(SortMixin):
    default_sort_params = ('book_copy__book__title', 'asc')
    allowed_sort_params = ['book_copy__book__title', 'borrower__username','beginning_date','end_date']
    model = Lending
    template_name="sharing/lending_list.html"
    paginate_by = 50

class LendingOnGoingList(LendingAllList):
    queryset = Lending.objects.filter(actual_lending())

class LendingCreate(SuccessMessageMixin, CreateView):
    model = Lending
    form_class = LendingForm
    success_url = reverse_lazy('lending_list')
    success_message = _("The lending of %(book_copy)s to %(borrower)s was created successfully")
    def form_valid(self, form):
        lending = form.save()
        remove_from_queue(lending.book_copy,lending.borrower,lending)
        return redirect('book_detail',book_id=lending.book_copy.book.id)

class LendingBookCreate(LendingCreate):
    form_class = None
    fields = ['borrower','beginning_date']
    def form_valid(self, form):
        lending = form.save(commit=False)
        lending.book_copy = get_object_or_404(Ownership,pk=self.kwargs['book_id'])
        if is_lending_possible(lending.beginning_date,lending.book_copy):
            lending.save()
            remove_from_queue(lending.book_copy,lending.borrower,lending)
        else:
            messages.add_message(self.request,messages.ERROR,_("This lending is not possible and you should have had errors on the form!"))

        return redirect('book_detail',book_id=lending.book_copy.book.id)

class BorrowingCreate(LendingCreate):
    form_class = None
    fields = ['book_copy','beginning_date']
    def form_valid(self, form):
        lending = form.save(commit=False)
        lending.borrower = self.request.user
        if is_lending_possible(lending.beginning_date,lending.book_copy):
            lending.save()
            remove_from_queue(lending.book_copy,lending.borrower,lending)
        else:
            messages.add_message(self.request,messages.ERROR,_("This lending is not possible and you should have had errors on the form!"))

        return redirect('book_detail',book_id=lending.book_copy.book.id)

class BorrowingBookCreate(LendingCreate):
    form_class = None
    fields = ['beginning_date']
    
    def form_valid(self, form):
        lending = form.save(commit=False)
        lending.borrower = self.request.user
        lending.book_copy = get_object_or_404(Ownership,pk=self.kwargs['book_id'])
        if is_lending_possible(lending.beginning_date,lending.book_copy):
            lending.save()
            remove_from_queue(lending.book_copy,lending.borrower,lending)
        else:
            messages.add_message(self.request,messages.ERROR,_("This lending is not possible and you should have had errors on the form!"))

        return redirect('book_detail',book_id=lending.book_copy.book.id)

class LendingUpdate(SuccessMessageMixin, UpdateView):
    model = Lending
    success_url = reverse_lazy('lending_list')
    success_message = _("The lending of %(book_copy)s to %(borrower)s was updated successfully")
    fields = ['book_copy','borrower','beginning_date','end_date']

class LendingDelete(DeleteView):
    model = Lending
    template_name="sharing/lending_confirm_delete.html"
    success_url = reverse_lazy('lending_list')

@permission_required('add_user')
def member_add(request):
    """
    Show a member profile and his sharing history.
    """
    if request.method == "POST":
        profile = Profile()
        form_user = UserForm(request.POST)
        form_profile = ProfileForm(request.POST)
        if form_user.is_valid() and form_profile.is_valid():
            confirm_password = form_user.cleaned_data['confirm_password']
            if confirm_password == form_user.cleaned_data['password']:
                user = User.objects.create_user(form_user.cleaned_data['username'], form_user.cleaned_data['email'], form_user.cleaned_data['password'])
                profile.user = user
                profile.save()
                messages.add_message(request, messages.SUCCESS, _("The new user has been successfully added !"))
                form_user = UserForm()
                form_profile = ProfileForm()
            else:
                messages.add_message(request, messages.ERROR, _("The two passwords are different."))
    else:
        form_user = UserForm()
        form_profile = ProfileForm()
    return render(request, 'sharing/member_form.html', {'form_user':form_user,'form_profile':form_profile})

@login_required()
def lending_end(request, lending_id):
    """
    Finishes the lending and adds a finish date.
    """
    lending = get_object_or_404(Lending, pk=lending_id)
    if request.method == 'POST':
        form = LendingEndForm(request.POST,instance=lending)
        if form.is_valid():
            queues = Queue.objects.filter(book_copy__id=lending.book_copy.id).order_by('added_date').all()
            if len(queues) > 0:
                # send an email to queue 0
                if queues[0].borrower.email:
                    
                    d = Context({ 'book_copy': lending.book_copy })
                    plaintext_mail = get_template('mails/sharing/queue_book_ready.txt').render(d)
                    html_mail = get_template('mails/sharing/queue_book_ready.html').render(d)

                    send_mail('Your book is ready !','no-reply@bibl-io.fr',plaintext_mail.replace("\n",""),[queues[0].borrower.email],html_message=html_mail, fail_silently=False)
            form.save()
            messages.add_message(request, messages.SUCCESS, _('The lending has been updated and the new end date is now %s.' % lending.end_date))
            return redirect('book_detail',book_id=lending.book_copy.book.id)
    else:
        form = LendingEndForm(instance=lending)
    return render(request, 'sharing/lending_form.html', {'form':form})


def log_in(request):
    """
    Log in a member.
    """
    error = False
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)

                profile = Profile.objects.get(user=user)
                translation_activate(profile.locale)
                request.session[LANGUAGE_SESSION_KEY] = profile.locale

                redirect_url = request.GET.get('next')
                if redirect_url:
                    return redirect(redirect_url)
            else:
                error = True
    else:
        form = LogInForm()

    return render(request, 'base/login.html', locals())

@login_required()
def log_out(request):
    """
    Log out a member.
    """
    logout(request)
    return redirect(reverse('book_list'))

@login_required()
def profile_edit(request):
    """
    Show a member's profile and allows him to edit it.
    """
    profile = get_object_or_404(Profile, user__id=request.user.id)
    if request.method == "POST":
        form_user = UserEditForm(request.POST,instance=request.user)
        form_profile = ProfileForm(request.POST, request.FILES,instance=profile)
        if form_user.is_valid() and form_profile.is_valid():
            confirm_password = form_user.cleaned_data['confirm_password']
            password = form_user.cleaned_data['password']
            # Either both passwords have been sent and are equal
            # Or none has been sent
            if ( not confirm_password and not password ) or confirm_password == password:
                user = form_user.save(commit=False)
                # Only update password if both have been sent otherwise it will logout the user.
                if confirm_password and password:
                    user.set_password(password)
                    user.save()
                    user = authenticate(username=user.username, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                # We otherwise save the email modifications.
                else:
                    user.save()
                profile = form_profile.save()
                translation_activate(profile.locale)
                request.session[LANGUAGE_SESSION_KEY] = profile.locale
                

                messages.add_message(request, messages.SUCCESS, _('Your profile has been successfully updated !'))
                return redirect(reverse('profile_show',args=[request.user.id]))
            else:
                messages.add_message(request, messages.ERROR, _('The two passwords are different or you forgot one.'))
    else:
        form_user = UserEditForm(instance=request.user)
        form_profile = ProfileForm(instance=profile)
    return render(request, 'sharing/member_form.html', {'form_user':form_user,'form_profile':form_profile})

@login_required()
def profile_show(request, profile_id):
    """
    Show a member profile and his sharing history.
    """
    profile = get_object_or_404(Profile, user__pk=profile_id)
    borrowings = Lending.objects.filter(actual_lending(),borrower__id=profile.user.id)
    lendings = Lending.objects.filter(actual_lending(),book_copy__owner__id=profile.user.id)
    books = Book.objects.filter(owners__id=profile.user.id)
    
    return render(request, 'sharing/profile_show.html', locals())

@login_required()
def my_dashboard(request):
    """
    Show a member dashboard.
    """
    profile = get_object_or_404(Profile, user__pk=request.user.id)
    borrowings = Lending.objects.filter(actual_lending(),borrower__id=profile.user.id)
    lendings = Lending.objects.filter(actual_lending(),book_copy__owner__id=profile.user.id)
    books = Book.objects.filter(owners__id=profile.user.id)
    
    return render(request, 'sharing/dashboard.html', locals())

class BorrowerList(SortMixin):
    default_sort_params = ('user__username', 'asc')
    allowed_sort_params = ['user__username','phone_number']
    model = Profile
    template_name="sharing/borrower_list.html"
    paginate_by = 20




class QueueList(SortMixin):
    context_object_name = "queues"
    default_sort_params = ('updated_date', 'desc')
    allowed_sort_params = ['title', 'author__lastname', 'added_date', 'updated_date']
    model = Queue
    template_name="sharing/queue_list.html"
    paginate_by = 30

class QueueCreate(SuccessMessageMixin, CreateView):
    model = Queue
    success_url = reverse_lazy('queue_list')
    success_message = _("%(book_copy)s was added successfully")
    fields = ['book_copy','borrower']
    def form_valid(self, form):
        queue = form.save(commit=False)
        if is_queueing_possible(queue.book_copy,queue.borrower):
            messages.add_message(self.request,messages.ERROR,_("You are already waiting for this book. Delete your previous demand before doing a new one!"))
        else:
            queue.save()
            messages.add_message(self.request,messages.SUCCESS,_("You have been successfully added to the queue for this book!"))
        return redirect('book_detail',book_id=queue.book_copy.book.id)

class QueueToBookCreate(SuccessMessageMixin, CreateView):
    model = Queue
    success_url = reverse_lazy('queue_list')
    success_message = _("%(book_copy)s was added successfully")
    fields = []
    def form_valid(self, form):
        queue = form.save(commit=False)
        queue.borrower = self.request.user
        queue.book_copy = get_object_or_404(Ownership,pk=self.kwargs['ownership_id'])
        if is_queueing_possible(queue.book_copy,queue.borrower):
            messages.add_message(self.request,messages.ERROR,_("You are already waiting for this book. Delete your previous demand before doing a new one!"))
        else:
            queue.save()
            messages.add_message(self.request,messages.SUCCESS,_("You have been successfully added to the queue for this book!"))
        return redirect('book_detail',book_id=queue.book_copy.book.id)

class QueueUpdate(SuccessMessageMixin, UpdateView):
    model = Queue
    success_url = reverse_lazy('queue_list')
    success_message = _("%(book_copy)s was updated successfully")
    fields = ['book_copy','borrower', 'fulfilled', 'lending']

class QueueDelete(DeleteView):
    model = Queue
    template_name="sharing/queue_confirm_delete.html"
    success_url = reverse_lazy('queue_list')
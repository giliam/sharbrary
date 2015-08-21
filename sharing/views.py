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
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from sharing.models import Lending, Profile
from sharing.forms import LendingEndForm, LogInForm, LendingForm, ProfileForm, UserForm,UserEditForm
from library.models import Book, Ownership

from utils.models.sortmixin import SortMixin
from utils.models.conditions import actual_lending
from utils.models.availability import determine_book_availability

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
    

class LendingBookCreate(LendingCreate):
    form_class = None
    fields = ['borrower','beginning_date']
    def form_valid(self, form):
        lending = form.save(commit=False)
        lending.book_copy = get_object_or_404(Ownership,pk=self.kwargs['book_id'])
        if is_lending_possible(lending.beginning_date,lending.book_copy):
            lending.save()
        else:
            messages.add_message(request,messages.ERROR,_("This lending is not possible and you should have had errors on the form!"))

        return redirect('book_list')

class BorrowingCreate(LendingCreate):
    form_class = None
    fields = ['book_copy','beginning_date']
    def form_valid(self, form):
        lending = form.save(commit=False)
        lending.borrower = self.request.user
        if is_lending_possible(lending.beginning_date,lending.book_copy):
            lending.save()
        else:
            messages.add_message(request,messages.ERROR,_("This lending is not possible and you should have had errors on the form!"))

        return redirect('book_list')

class BorrowingBookCreate(LendingCreate):
    form_class = None
    fields = ['beginning_date']
    
    def form_valid(self, form):
        lending = form.save(commit=False)
        lending.borrower = self.request.user
        lending.book_copy = get_object_or_404(Ownership,pk=self.kwargs['book_id'])
        if is_lending_possible(lending.beginning_date,lending.book_copy):
            lending.save()
        else:
            messages.add_message(request,messages.ERROR,_("This lending is not possible and you should have had errors on the form!"))

        return redirect('book_list')

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
            form.save()
            messages.add_message(request, messages.SUCCESS, _('The lending has been updated and the new end date is now %s.' % lending.end_date))
            return redirect('lending_list')
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
                profile = form_profile.save()
                

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


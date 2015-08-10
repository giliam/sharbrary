from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from sharing.models import Lending, Profile
from sharing.forms import LendingForm, LogInForm
from library.models import Book

from utils.models.sortmixin import SortMixin
from utils.models.conditions import actual_lending

class LendingAllList(SortMixin):
    default_sort_params = ('book__title', 'asc')
    allowed_sort_params = ['book__title', 'borrower__username','status','beginning_date','end_date']
    model = Lending
    template_name="sharing/lending_list.html"
    paginate_by = 50

class LendingOnGoingList(LendingAllList):
    queryset = Lending.objects.filter(actual_lending())

class LendingCreate(SuccessMessageMixin, CreateView):
    model = Lending
    success_url = reverse_lazy('lending_list')
    success_message = _("The lending of %(book)s to %(borrower)s was created successfully")
    fields = ['book','borrower','status','beginning_date','end_date']

class LendingUpdate(SuccessMessageMixin, UpdateView):
    model = Lending
    success_url = reverse_lazy('lending_list')
    success_message = _("The lending of %(book)s to %(borrower)s was updated successfully")
    fields = ['book','borrower','status','beginning_date','end_date']

class LendingDelete(DeleteView):
    model = Lending
    template_name="sharing/lending_confirm_delete.html"
    success_url = reverse_lazy('lending_list')

@login_required()
def lending_end(request, lending_id):
    """
    Finishes the lending and adds a finish date.
    """
    lending = get_object_or_404(Lending, pk=lending_id)
    if request.method == 'POST':
        form = LendingForm(request.POST,instance=lending)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'The lending has been updated and the new end date is now %s.' % lending.end_date)
            return redirect('lending_list')
    else:
        form = LendingForm(instance=lending)
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
def profile_show(request, profile_id):
    """
    Show a member profile and his sharing history.
    """
    profile = get_object_or_404(Profile, user__pk=profile_id)
    borrowings = Lending.objects.filter(actual_lending(),borrower__id=profile.user.id)
    lendings = Lending.objects.filter(actual_lending(),book__owner__id=profile.user.id)
    books = Book.objects.filter(owner__id=profile.user.id)
    
    return render(request, 'sharing/profile_show.html', locals())

class BorrowerList(SortMixin):
    default_sort_params = ('user__username', 'asc')
    allowed_sort_params = ['user__username','phone_number']
    model = Profile
    template_name="sharing/borrower_list.html"
    paginate_by = 20


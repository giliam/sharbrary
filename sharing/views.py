from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages

from sharing.models import Lending
from sharing.forms import LendingForm

class LendingList(ListView):
    model = Lending
    template_name="sharing/lending_list.html"

class LendingCreate(CreateView):
    model = Lending
    success_url = reverse_lazy('lending_list')
    fields = ['book','borrower','status','beginning_date','end_date']

class LendingUpdate(UpdateView):
    model = Lending
    success_url = reverse_lazy('lending_list')
    fields = ['book','borrower','status','beginning_date','end_date']

class LendingDelete(DeleteView):
    model = Lending
    template_name="sharing/lending_confirm_delete.html"
    success_url = reverse_lazy('lending_list')

"""
Finishes the lending and adds a finish date.
"""
def end_lending(request, lending_id):
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

class BorrowerList(ListView):
    model = User
    template_name="sharing/borrower_list.html"



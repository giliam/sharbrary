from django.shortcuts import render
from sharing.models import Lending
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

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
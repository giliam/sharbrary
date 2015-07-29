from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from bibliotheque.models import Livre

class LivreList(ListView):
    model = Livre

class LivreCreate(CreateView):
    model = Livre
    success_url = reverse_lazy('livre_liste')
    fields = ['name', 'ip', 'order']

class LivreUpdate(UpdateView):
    model = Livre
    success_url = reverse_lazy('livre_liste')
    fields = ['name', 'ip', 'order']

class LivreDelete(DeleteView):
    model = Livre
    success_url = reverse_lazy('livre_liste')

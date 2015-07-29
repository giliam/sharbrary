from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from bibliotheque.models import Livre

class LivreList(ListView):
    model = Livre
    template_name="bibliotheque/livre_liste.html"

class LivreCreate(CreateView):
    model = Livre
    success_url = reverse_lazy('livre_liste')
    fields = ['titre', 'annee_parution']

class LivreUpdate(UpdateView):
    model = Livre
    success_url = reverse_lazy('livre_liste')
    fields = ['titre', 'annee_parution']

class LivreDelete(DeleteView):
    model = Livre
    template_name="bibliotheque/livre_confirme_suppression.html"
    success_url = reverse_lazy('livre_liste')

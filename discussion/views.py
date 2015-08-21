# coding: utf-8
from django.shortcuts import render
from django.views.generic import TemplateView,ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from utils.models.sortmixin import SortMixin

from discussion.models import Discussion, Message

def discussion_detail(request, discussion_id):
    """
    Shows discussion details.
    """
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    messages = Message.objects.filter(discussion__id=discussion_id)
    return render(request, 'discussion/discussion_detail.html', {'discussion':discussion,'messages':messages})

class DiscussionList(SortMixin):
    context_object_name = "discussions"
    default_sort_params = ('updated_date', 'desc')
    allowed_sort_params = ['title', 'author__lastname', 'added_date', 'updated_date']
    model = Discussion
    template_name="discussion/discussion_list.html"
    paginate_by = 30

class DiscussionCreate(SuccessMessageMixin, CreateView):
    model = Discussion
    success_url = reverse_lazy('discussion_list')
    success_message = _("%(title)s was added successfully")
    fields = ['title']

class DiscussionUpdate(SuccessMessageMixin, UpdateView):
    model = Discussion
    success_url = reverse_lazy('discussion_list')
    success_message = _("%(title)s was updated successfully")
    fields = ['title']

class DiscussionDelete(DeleteView):
    model = Discussion
    template_name="discussion/discussion_confirm_delete.html"
    success_url = reverse_lazy('discussion_list')

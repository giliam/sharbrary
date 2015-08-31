# coding: utf-8
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from utils.models.sortmixin import SortMixin

from discussion.models import Discussion, Message

from utils.models.authorizations import CheckOwner

def discussion_detail(request, discussion_id):
    """
    Shows discussion details.
    """
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    messages_discussion = Message.objects.filter(discussion__id=discussion_id)
    return render(request, 'discussion/discussion_detail.html', {'discussion':discussion,'messages_discussion':messages_discussion})

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

    def form_valid(self, form):
        discussion = form.save(commit=False)
        discussion.author = self.request.user
        discussion.save()
        return redirect('discussion_detail',discussion_id=discussion.id)

class DiscussionUpdate(SuccessMessageMixin, UpdateView, CheckOwner):
    model = Discussion
    success_url = reverse_lazy('discussion_list')
    success_message = _("%(title)s was updated successfully")
    fields = ['title']
    owner_field = 'author'

class DiscussionDelete(DeleteView):
    model = Discussion
    template_name="discussion/discussion_confirm_delete.html"
    success_url = reverse_lazy('discussion_list')

class MessageCreate(SuccessMessageMixin, CreateView):
    model = Message
    success_url = reverse_lazy('discussion_list')
    success_message = _("%(title)s was added successfully")
    fields = ['message']

    def form_valid(self, form):
        message = form.save(commit=False)
        message.author = self.request.user
        message.discussion = get_object_or_404(Discussion,pk=self.kwargs['discussion_id'])
        message.save()
        return redirect('discussion_detail',discussion_id=message.discussion.id)

class MessageUpdate(SuccessMessageMixin, UpdateView, CheckOwner):
    model = Message
    success_url = reverse_lazy('discussion_list')
    success_message = _("The message was updated successfully")
    fields = ['message']
    owner_field = 'author'    

class MessageDelete(DeleteView, CheckOwner):
    model = Message
    template_name="discussion/discussion_confirm_delete.html"
    success_url = reverse_lazy('discussion_list')
    owner_field = 'author'
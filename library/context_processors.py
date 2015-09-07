# coding: utf-8
from sharing.models import Profile

from library.forms import ResearchForm
from library.models import Page

from sharbrary.settings import MEDIA_URL, STATIC_URL

from django.utils.translation import ugettext_lazy as _

def urls_processor(request):
    return {'MEDIA_URL': MEDIA_URL,'STATIC_URL': STATIC_URL}

def profiles_processor(request):
    try:
        profile = Profile.objects.get(user__id=request.user.id)
    except:
        profile = None
    return {'request_profile': profile}

def research_form_processor(request):
    return {'form_research': ResearchForm()}

def header_processor(request):
    try:
        header_title = Page.objects.get(name='header_title')
    except Page.DoesNotExist:
        header_title = {
            'title':"Sharbrary",
            'content':_("A library online for sharing books between friends.")
        }
    return {'header_title':header_title}
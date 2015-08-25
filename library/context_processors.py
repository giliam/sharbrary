# coding: utf-8
from sharing.models import Profile

from library.forms import ResearchForm

from sharbrary.settings import MEDIA_URL, STATIC_URL

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
from django import forms
from django.utils.translation import ugettext_lazy as _

from library.models import Book
from django.contrib.auth.models import User

class SelectOwnerForm(forms.Form):
    owners = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        owners = kwargs.pop('owners', None)
        super(SelectOwnerForm, self).__init__(*args, **kwargs)

        if owners:
            self.fields['owners'].queryset = owners

class ResearchForm(forms.Form):
    research = forms.CharField(max_length=100)
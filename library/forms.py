from django import forms
from django.utils.translation import ugettext_lazy as _

from library.models import Book
from sharing.models import Profile

class SelectOwnerForm(forms.Form):
    owners = forms.ModelMultipleChoiceField(queryset=Profile.objects.all())

    def __init__(self, *args, **kwargs):
        owners = kwargs.pop('owners', None)
        super(SelectOwnerForm, self).__init__(*args, **kwargs)

        if owners:
            self.fields['owners'].queryset = owners
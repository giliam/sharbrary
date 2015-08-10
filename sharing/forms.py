from django import forms
from models import Lending
from django.utils.translation import ugettext_lazy as _

class LendingForm(forms.ModelForm):
    class Meta:
        model = Lending
        fields = ('end_date',)

class LogInForm(forms.Form):
    username = forms.CharField(label=_("username").capitalize(), max_length=30)
    password = forms.CharField(label=_("password").capitalize(), widget=forms.PasswordInput)
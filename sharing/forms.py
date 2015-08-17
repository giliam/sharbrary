from django import forms
from models import Lending
from django.utils.translation import ugettext_lazy as _

class LendingEndForm(forms.ModelForm):
    class Meta:
        model = Lending
        fields = ('end_date',)

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if self.instance.beginning_date > end_date:
            raise forms.ValidationError(_("The end date must be after the beginning date."))
        return end_date


class LogInForm(forms.Form):
    username = forms.CharField(label=_("username").capitalize(), max_length=30)
    password = forms.CharField(label=_("password").capitalize(), widget=forms.PasswordInput)
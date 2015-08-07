from django import forms
from models import Lending

class LendingForm(forms.ModelForm):
    class Meta:
        model = Lending
        fields = ('end_date',)
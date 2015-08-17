from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from sharing.models import Lending


class LendingEndForm(forms.ModelForm):
    class Meta:
        model = Lending
        fields = ('end_date',)

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if self.instance.beginning_date > end_date:
            raise forms.ValidationError(_("The end date must be after the beginning date."))
        return end_date

class LendingForm(forms.ModelForm):
    class Meta:
        model = Lending
        fields = ('book', 'borrower', 'beginning_date',)

    def clean(self):
        beginning_date = self.cleaned_data['beginning_date']
        book = self.cleaned_data['book']
        lendings = Lending.objects.filter(Q(beginning_date__lte=beginning_date,end_date__gte=beginning_date,book__id=book.id)|
        Q(beginning_date__lte=beginning_date,end_date=None,book__id=book.id))
        print lendings.all()
        if lendings:
            raise forms.ValidationError(_("This book is already borrowed !"))
        return beginning_date


class LogInForm(forms.Form):
    username = forms.CharField(label=_("username").capitalize(), max_length=30)
    password = forms.CharField(label=_("password").capitalize(), widget=forms.PasswordInput)
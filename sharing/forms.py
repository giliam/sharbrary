from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django.shortcuts import get_object_or_404

from sharing.models import Lending, Profile
from library.models import Book

from utils.models.availability import determine_book_availability

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
        if determine_book_availability(beginning_date,book):
            raise forms.ValidationError(_("This book is already borrowed !"))
        return self.cleaned_data

class LogInForm(forms.Form):
    username = forms.CharField(label=_("username").capitalize(), max_length=30)
    password = forms.CharField(label=_("password").capitalize(), widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('informations', 'phone_number',)

# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django.shortcuts import get_object_or_404

from sharing.models import Lending, Profile
from library.models import Book

from utils.models.availability import is_lending_possible, is_returning_possible

class LendingEndForm(forms.ModelForm):
    class Meta:
        model = Lending
        fields = ('end_date',)

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if self.instance.beginning_date > end_date:
            raise forms.ValidationError(_("The end date must be after the beginning date."))
        is_returning_possible(end_date,self.instance)
        return end_date

class LendingForm(forms.ModelForm):
    class Meta:
        model = Lending
        fields = ('book_copy', 'borrower', 'beginning_date',)

    def clean(self):
        beginning_date = self.cleaned_data['beginning_date']
        book_copy = self.cleaned_data['book_copy']
        is_lending_possible(beginning_date,book_copy)
        return self.cleaned_data

class LogInForm(forms.Form):
    username = forms.CharField(label=_("Username"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(label=_("Confirm password"),widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserEditForm(forms.ModelForm):
    password = forms.CharField(label=_("Password"),widget=forms.PasswordInput(),required=False)
    confirm_password = forms.CharField(label=_("Confirm password"),widget=forms.PasswordInput(),required=False)
    class Meta:
        model = User
        fields = ('email', 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('informations', 'phone_number', 'picture','locale',)

import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class SearchForm(forms.Form):
    name_field = forms.CharField(max_length=200, required=True)

class SignInForm(forms.Form):
    user_email = forms.CharField(max_length=200, required=True)
    user_password = forms.CharField(max_length=200, required=True)
    user_login = forms.CharField(max_length=200, required=True)

class SignUpForm(forms.Form):
    
    user_email = forms.CharField(max_length=200, required=True)
    user_email_1 = forms.CharField(max_length=200, required=True)
    user_password = forms.CharField(max_length=200, required=True)
    user_password_1 = forms.CharField(max_length=200, required=True)
    user_name = forms.CharField(max_length=200, required=True)
    user_surname = forms.CharField(max_length=200, required=True)
    
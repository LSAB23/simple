from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email


def validate(password):
    return validate_password(password)

class Signup(forms.Form):
    name = forms.CharField(label='Name', max_length=256, required=True)
    email = forms.EmailField(label='Email',max_length=320, required=True, validators=[validate_email])
    password = forms.CharField(label='Password',widget=forms.PasswordInput, required=True, validators=[validate])

class Login(forms.Form):
    email = forms.EmailField(label='Email',max_length=320, required=True, validators=[validate_email])
    password = forms.CharField(label='Password',widget=forms.PasswordInput, required=True)

class Change(forms.Form):
    Old_Password = forms.CharField(label='Old Password',widget=forms.PasswordInput, required=True)
    New_Password = forms.CharField(label='New Password',widget=forms.PasswordInput, required=True, validators=[validate])
    New_Password_Again = forms.CharField(label='New Password Again',widget=forms.PasswordInput, required=True, validators=[validate])
    

class Reset(forms.Form):
    Email = forms.EmailField(label='Email', required=True, validators=[validate_email])

class PasswordReset(forms.Form):
    New_Password= forms.CharField(label='New Password', required=True, validators=[validate])
    Password_Again = forms.CharField(label='Password Again', required=True, validators=[validate])
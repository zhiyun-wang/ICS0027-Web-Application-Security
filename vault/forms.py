from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class EntryForm(forms.Form):
    website = forms.CharField(max_length=150)
    account_username = forms.CharField(max_length=200, label='Account username')
    account_password = forms.CharField(max_length=500, widget=forms.PasswordInput(render_value=False), label='Account password')
    master_password = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Master password')

class UnlockForm(forms.Form):
    master_password = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Master password')

from django import forms
from django.contrib.auth.models import User

class RegistratioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password", required=False)
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
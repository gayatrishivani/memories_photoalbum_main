from django import forms
from .models import User

class UserForm(forms.ModelForm):

    username = forms.CharField(max_length=80)
    email = forms.EmailField(max_length=255)
    password = forms.CharField(min_length=6,widget=forms.PasswordInput())
    confirm_password = forms.CharField(min_length=6,widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email','password')

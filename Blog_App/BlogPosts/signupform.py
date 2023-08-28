


from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm




class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']



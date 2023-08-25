from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']  # Add other fields you want to update


class CompositeUpdateForm(UserProfileUpdateForm):
    email = forms.EmailField(max_length=254)
    email_confirm = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_confirm = cleaned_data.get('email_confirm')

        if email and email_confirm and email != email_confirm:
            raise forms.ValidationError("Emails do not match.")

from django import forms
from .models import UserProfile

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']  # Add other fields you want to update




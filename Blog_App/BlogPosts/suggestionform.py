from django import forms
from .models import Suggestion,SuggestionReply

class SuggestionForm(forms.ModelForm):
    title = forms.CharField(max_length=30)
    class Meta:
        model = Suggestion
        fields = ('title','text')

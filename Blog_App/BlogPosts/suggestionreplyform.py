from django import forms
from .models import SuggestionReply
class SuggestionReplyForm(forms.ModelForm):
    class Meta:
        model = SuggestionReply
        fields = ('reply_text',)

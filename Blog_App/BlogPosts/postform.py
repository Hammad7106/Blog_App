
from ckeditor.widgets import CKEditorWidget

from .models import Post
from django import forms

class UserPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title', 'post_content', 'post_image']


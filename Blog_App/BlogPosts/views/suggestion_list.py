
from ..models import Post,Suggestion

from django.contrib.auth.decorators import login_required
from django.shortcuts import render



@login_required
def suggestions_list(request,post_id):
    post = Post.objects.get(pk=post_id)
    suggestions = Suggestion.objects.filter(post=post)
    return render(request, 'BlogApp/suggestion_list.html', {'suggestions': suggestions})


from ..models import Suggestion

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



@login_required
def apply_suggestion(request, suggestion_id):
    suggestion = Suggestion.objects.get(pk=suggestion_id)

    if suggestion.user != request.user:
        # Apply the suggestion to the post
        post = suggestion.post
        post.post_content = suggestion.text
        suggestion.status=True
        post.save()


    return redirect('suggestions_list', suggestion.post.id)

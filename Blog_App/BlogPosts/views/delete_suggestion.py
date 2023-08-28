
from django.shortcuts import get_object_or_404

from ..models import Suggestion

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def delete_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, pk=suggestion_id)

    if suggestion.post.user == request.user:
        suggestion.delete()

    return redirect('suggestions_list', post_id=suggestion.post.id)

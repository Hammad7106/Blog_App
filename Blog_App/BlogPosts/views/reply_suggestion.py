
from ..models import Suggestion

from ..suggestionreplyform import SuggestionReplyForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect





@login_required
def reply_suggestion(request, suggestion_id):
    suggestion = Suggestion.objects.get(pk=suggestion_id)

    if request.method == 'POST':
        form = SuggestionReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.suggestion = suggestion
            reply.save()
            return redirect('suggestions_list', suggestion.post.id)
    else:
        form = SuggestionReplyForm()

    return render(request, 'BlogApp/reply_suggestion.html', {'suggestionreplyform': form})

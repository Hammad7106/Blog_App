
from ..models import Post
from ..suggestionform import SuggestionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
class SubmitSuggestionView(View):
    @method_decorator(login_required())
    def get(self, request, post_id=None, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)

        form = SuggestionForm(initial={'text': post.post_content, 'title': post.post_title})
        return render(request, 'BlogApp/submit_suggestion.html', {'suggestionform': form})

    @method_decorator(login_required())
    def post(self, request, post_id=None, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)

        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.post = post  # Set the post field
            suggestion.save()
            return redirect('list')

        return render(request, 'BlogApp/submit_suggestion.html', {'suggestionform': form})


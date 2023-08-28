
from django.shortcuts import get_object_or_404

from ..models import Post,Comments
from django.views.generic import  CreateView
from django.urls import reverse_lazy

from ..comments import CommentForm

class AddComment(CreateView):
    model = Comments
    form_class = CommentForm
    template_name = 'BlogApp/comments.html'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        post_id = self.kwargs['pk']  # or self.kwargs['post_id'] based on your URL pattern
        post = get_object_or_404(Post, pk=post_id)

        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = post  # Associate the comment with the post
        comment.save()

        return super().form_valid(form)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['files'] = self.request.FILES
        return kwargs


from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Post,Comments
from django.views.generic import ListView

class UserPostListView(ListView,LoginRequiredMixin):
    model = Post
    template_name = 'BlogApp/postlist.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch comments for each post and add them to the context
        for post in context['posts']:
            comments = Comments.objects.filter(post=post)
            post.comments = comments
        return context

    def get_queryset(self):
        return Post.objects.filter(approved=True)






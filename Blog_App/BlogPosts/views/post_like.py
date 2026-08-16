
from django.shortcuts import get_object_or_404

from django.views import View
from ..models import Post

from django.http import JsonResponse


class LikeView(View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, id=pk)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
        else:
            post.liked_by.add(request.user)
        return JsonResponse({'like_count': post.liked_by.count()})

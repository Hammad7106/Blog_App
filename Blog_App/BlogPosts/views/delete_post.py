
from django.shortcuts import get_object_or_404

from ..models import Post

from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.user:
        post.delete()
    return redirect('list')

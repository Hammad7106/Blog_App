
from ..models import Post

from ..models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect






@login_required
def delete_unapproved_post(request):
    if not UserProfile.objects.filter(user=request.user, role=UserProfile.UserRoleEnum.MODERATOR.value).exists():
        return redirect('Dashboard')

    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        post.delete()

    return redirect('list')

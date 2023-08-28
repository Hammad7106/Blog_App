
from ..models import Post

from ..models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect



@login_required
def approve_posts(request):
    if not UserProfile.objects.filter(user=request.user, role=UserProfile.UserRoleEnum.MODERATOR.value).exists():
        return redirect('approve_posts')

    pending_posts = Post.objects.filter(approved=False)

    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        post.approved = True
        post.save()

    return render(request, 'BlogApp/approve_posts.html', {'pending_posts': pending_posts})

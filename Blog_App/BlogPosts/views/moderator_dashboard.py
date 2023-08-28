
from ..models import Post

from ..models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect




@login_required
def moderator_dashboard(request):
    if not UserProfile.objects.filter(user=request.user, role=UserProfile.UserRoleEnum.MODERATOR.value).exists():
        return redirect('moderator_dashboard')

    reported_posts = Post.objects.filter(reported_by__isnull=False).distinct()  # Get posts with reports

    return render(request, 'BlogApp/moderator_dashboard.html', {'reported_posts': reported_posts})

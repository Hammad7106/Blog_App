

from django.shortcuts import get_object_or_404

from ..models import Comments, CommentLike

from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect


from django.http import JsonResponse



@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    action = None

    if request.user not in comment.liked_by.all():
        CommentLike.objects.create(user=request.user, comment=comment)
        comment.liked_by.add(request.user)
        action = 'liked'
    else:
        like = CommentLike.objects.get(user=request.user, comment=comment)
        like.delete()
        comment.liked_by.remove(request.user)
        action = 'unliked'

    like_count = comment.liked_by.count()  # Get updated like count
    return JsonResponse({'status': 'success', 'action': action, 'like_count': like_count})



@login_required
def unlike_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    action = None

    if request.user in comment.liked_by.all():
        like = CommentLike.objects.get(user=request.user, comment=comment)
        like.delete()
        comment.liked_by.remove(request.user)
        action = 'unliked'

    like_count = comment.liked_by.count()  # Get updated like count
    return JsonResponse({'status': 'success', 'action': action, 'like_count': like_count})






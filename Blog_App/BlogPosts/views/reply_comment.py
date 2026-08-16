
from django.shortcuts import get_object_or_404

from ..models import Comments

from ..comments import CommentForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect




@login_required  # Ensure the user is logged in to reply
def reply_to_comment(request, comment_id):
    parent_comment = get_object_or_404(Comments, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.parent_comment = parent_comment  # Set the parent comment
            reply.post = parent_comment.post  # Attach the comment to the same post
            reply.save()
            return redirect('list')  # Redirect to post detail page
    else:
        form = CommentForm()

    return render(request, 'BlogApp/reply_comment.html', {'comments': form})

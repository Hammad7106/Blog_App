
from cloudinary.uploader import upload

from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

from ..models import Comments

from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect



@login_required
def report_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    if request.user not in comment.reported_by.all():
        comment.reported_by.add(request.user)
    return redirect('list')  # Redirect to the same page after reporting

@login_required
def unreport_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    if request.user in comment.reported_by.all():
        comment.reported_by.remove(request.user)
    return redirect('list')  # Redirect to the same page after unreporting

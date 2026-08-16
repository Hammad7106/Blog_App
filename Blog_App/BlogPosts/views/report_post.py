
from django.shortcuts import get_object_or_404

from ..models import Post

from django.http import HttpResponseBadRequest

from django.shortcuts import redirect




def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.reported_by.add(request.user)  # Add the user to the 'reported_by' field
        return redirect('list')
    else:
        return HttpResponseBadRequest("Bad Request")

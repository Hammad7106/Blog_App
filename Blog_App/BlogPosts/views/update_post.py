
from django.shortcuts import get_object_or_404

from ..postform import UserPost

from ..models import Post

from django.shortcuts import render, redirect




def update_post(request, post_id):
    print("In Update View")
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.user:
        return redirect('list')


    if request.method == 'POST':
        form = UserPost(request.POST,request.FILES, instance=post)
        print(post)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = UserPost(instance=post)
    return render(request, 'BlogApp/update_post.html', {'postform': form,'post': post})


from django.views import View
from ..models import Like

from django.http import JsonResponse



class CheckLikeView(View):
    def get(self, request, post_id):
        user_liked = False
        # Assuming Like model has a field 'user' for the user who liked the post
        if request.user.is_authenticated:
            user_liked = Like.objects.filter(user=request.user, post_id=post_id).exists()
        return JsonResponse({'user_liked': user_liked})

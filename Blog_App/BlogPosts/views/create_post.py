from cloudinary.uploader import upload

from django.contrib.auth.mixins import LoginRequiredMixin

from ..postform import UserPost

from ..models import Post
from django.views.generic import  CreateView
from django.urls import reverse_lazy


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = UserPost
    template_name = 'BlogApp/Post.html'
    success_url = reverse_lazy('Dashboard')  # Replace with the actual URL name or path

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.approved = False

        # Upload post image to Cloudinary
        uploaded_file = self.request.FILES.get('post_image_field_name')  # Replace with your image field name
        if uploaded_file:
            result = upload(uploaded_file)  # Upload the image to Cloudinary
            form.instance.post_image = result['secure_url']  # Save the Cloudinary URL to the post_image field

        return super().form_valid(form)

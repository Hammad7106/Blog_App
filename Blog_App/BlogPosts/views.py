from cloudinary.uploader import upload

from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .loginform import LoginForm
from .signupform import SignUpForm
from .userprofileform import UserProfileForm
from .postform import UserPost
from django.views import View
from .models import Post,Like,Comments, CommentLike,Suggestion
from django.views.generic import ListView, CreateView,DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest
from django.db.models import Count
from .comments import CommentForm
from .suggestionform import SuggestionForm
from .suggestionreplyform import SuggestionReplyForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile
# Create your views here.
def Dashboard(request):
    return render(request,'BlogApp/base.html')




def Signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user is restricted and restriction duration has passed
        if 'restriction_start_timestamp' in request.session:
            restriction_duration = timedelta(minutes=1)  # Adjust as needed
            restriction_start_timestamp = request.session['restriction_start_timestamp']
            restriction_end_timestamp = restriction_start_timestamp + restriction_duration.total_seconds()
            current_timestamp = datetime.now().timestamp()

            if current_timestamp < restriction_end_timestamp:
                remaining_time = int(restriction_end_timestamp - current_timestamp)
                return render(request, "Blog_App/postlist.html", {'user_under_restriction': True, 'remaining_time_in_seconds': remaining_time})

            # If the restriction duration has passed, remove the session variable
            del request.session['restriction_start_timestamp']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.pop('failed_attempts', None)  # Reset failed attempts upon successful login
            return render(request, "BlogApp/base.html")
        else:
            if 'failed_attempts' not in request.session:
                request.session['failed_attempts'] = 0

            request.session['failed_attempts'] += 1

            if request.session['failed_attempts'] >= 3:
                request.session['restriction_start_timestamp'] = datetime.now().timestamp()  # Store restriction start timestamp
                messages.error(request, "You have attempted wrong credentials multiple times. You are now restricted from entering credentials for 1 minute.")
                return render(request, "BlogApp/login.html", {'user_under_restriction': True, 'remaining_time_in_seconds': 60})  # 180 seconds = 3 minutes

            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, "BlogApp/login.html", {'user_under_restriction': False})





class SignUpView(View):
    template_name = 'BlogApp/Sign_Up_Form.html'

    def get(self, request, *args, **kwargs):
        user_form = SignUpForm()
        profile_form = UserProfileForm()
        return render(request, self.template_name, {'signupform': user_form, 'userprofileform': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)

            # Upload profile image to Cloudinary
            uploaded_file = request.FILES.get('image_field_name')  # Replace with your image field name
            if uploaded_file:
                result = upload(uploaded_file)
                profile.image = result['secure_url']

            profile.user = user
            profile.save()
            return redirect('login')  # Redirect to a success page

        return render(request, self.template_name, {'signupform': user_form, 'userprofileform': profile_form})


# def loginuser(request):
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('list')
#             else:
#                 messages.error(request,"Invalid Authentication")
#     else:
#         form = LoginForm()
#
#     return render(request, 'BlogApp/login.html', {'loginform': form})




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





class UserPostListView(ListView,LoginRequiredMixin):
    model = Post
    template_name = 'BlogApp/postlist.html'
    context_object_name = 'posts'

    # def get_queryset(self):
    #     # Annotate each post with the count of likes
    #     queryset = super().get_queryset().annotate(like_count=Count('liked_by'))
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch comments for each post and add them to the context
        for post in context['posts']:
            comments = Comments.objects.filter(post=post)
            post.comments = comments
        return context

    def get_queryset(self):
        return Post.objects.filter(approved=True)




class PostdetailView(DetailView):
    model = Post
    template_name = 'BlogApp/postdetail.html'
    context_object_name = 'posts'

class LikeView(View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, id=pk)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
        else:
            post.liked_by.add(request.user)
        return JsonResponse({'like_count': post.liked_by.count()})



class AddComment(CreateView):
    model = Comments
    form_class = CommentForm
    template_name = 'BlogApp/comments.html'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        post_id = self.kwargs['pk']  # or self.kwargs['post_id'] based on your URL pattern
        post = get_object_or_404(Post, pk=post_id)

        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = post  # Associate the comment with the post
        comment.save()

        return super().form_valid(form)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['files'] = self.request.FILES
        return kwargs




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




@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.user:
        post.delete()
    return redirect('list')

@login_required
def delete_repo_post(request):
    if not UserProfile.objects.filter(user=request.user, role=UserProfile.UserRoleEnum.MODERATOR.value).exists():
        return redirect('Dashboard')

    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        post.delete()

    return redirect('moderator_dashboard')  # Redirect back to the moderator dashboard

@login_required
def delete_unapproved_post(request):
    if not UserProfile.objects.filter(user=request.user, role=UserProfile.UserRoleEnum.MODERATOR.value).exists():
        return redirect('Dashboard')

    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        post.delete()

    return redirect('list')


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




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .userprofileupdate import UserProfileUpdateForm,CompositeUpdateForm




@login_required
def profile_update(request):
    user = request.user


    if request.method == 'POST':
        form = CompositeUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('list')  # Redirect to the same page after update
    else:
        initial_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,

        }
        form = CompositeUpdateForm(initial=initial_data, instance=user)

    return render(request, 'BlogApp/profile_update.html', {'userprofileupdate': form})







def user_logout(reqeust):
    logout(reqeust)
    return redirect('login')


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
            return redirect('list', pk=parent_comment.post.id)  # Redirect to post detail page
    else:
        form = CommentForm()

    return render(request, 'BlogApp/reply_comment.html', {'comments': form})

@login_required
class CommentLikeView(View):
    def post(self, request, comment_id):
        try:
            comment = Comments.objects.get(id=comment_id)
            user = request.user

            # Check if the user has already liked the comment
            if CommentLike.objects.filter(user=user, comment=comment).exists():
                return JsonResponse({'error': 'You already liked this comment'})

            comment_like = CommentLike(user=user, comment=comment)
            comment_like.save()

            return JsonResponse({'success': 'Comment liked successfully'})
        except Comments.DoesNotExist:
            return JsonResponse({'error': 'Comment not found'})




def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.reported_by.add(request.user)  # Add the user to the 'reported_by' field
        return redirect('list', post_id=post_id)
    else:
        return HttpResponseBadRequest("Bad Request")

@login_required
def moderator_dashboard(request):
    if not UserProfile.objects.filter(user=request.user, role=UserProfile.UserRoleEnum.MODERATOR.value).exists():
        return redirect('moderator_dashboard')

    reported_posts = Post.objects.filter(reported_by__isnull=False).distinct()  # Get posts with reports

    return render(request, 'BlogApp/moderator_dashboard.html', {'reported_posts': reported_posts})

class CheckLikeView(View):
    def get(self, request, post_id):
        user_liked = False
        # Assuming Like model has a field 'user' for the user who liked the post
        if request.user.is_authenticated:
            user_liked = Like.objects.filter(user=request.user, post_id=post_id).exists()
        return JsonResponse({'user_liked': user_liked})


class CheckCommentLikeView(View):
    def get(self, request, comment_id):
        user_liked = False
        if request.user.is_authenticated:
            user_liked = CommentLike.objects.filter(user=request.user, comment_id=comment_id).exists()
        return JsonResponse({'user_liked': user_liked})




# THESE ARE THE SUGGESTION FUNCTIONS

@login_required
def submit_suggestion(request,post_id=None):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.save()
            return redirect('suggestions_list',post_id=post_id)
    else:
        post_content = Post.objects.get(id = post_id)
        form = SuggestionForm(initial={'text':post_content.post_content,'title':post_content})
    return render(request, 'BlogApp/submit_suggestion.html', {'suggestionform': form})



@login_required
def suggestions_list(request,post_id):
    post = Post.objects.get(pk=post_id)
    suggestions = Suggestion.objects.filter(post=post)
    return render(request, 'BlogApp/suggestion_list.html', {'suggestions': suggestions})


@login_required
def reply_suggestion(request, suggestion_id):
    suggestion = Suggestion.objects.get(pk=suggestion_id)

    if request.method == 'POST':
        form = SuggestionReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.suggestion = suggestion
            reply.save()
            return redirect('suggestions_list', suggestion.post.id)
    else:
        form = SuggestionReplyForm()

    return render(request, 'BlogApp/reply_suggestion.html', {'suggestionreplyform': form})


@login_required
def delete_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, pk=suggestion_id)

    if suggestion.post.user == request.user:
        suggestion.delete()

    return redirect('suggestions_list', post_id=suggestion.post.id)


@login_required
def apply_suggestion(request, suggestion_id):
    suggestion = Suggestion.objects.get(pk=suggestion_id)

    if suggestion.user != request.user:
        # Apply the suggestion to the post
        post = suggestion.post
        post.post_content = suggestion.text
        suggestion.status=True
        post.save()


    return redirect('suggestions_list', suggestion.post.id)

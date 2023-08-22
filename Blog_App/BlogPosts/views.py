from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .loginform import LoginForm
from .signupform import SignUpForm
from .userprofileform import UserProfileForm
from .postform import UserPost
from django.views import View
from .models import Post,Like,Comments,Report
from django.views.generic import ListView,UpdateView,CreateView,DetailView
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.db.models import Count
from .comments import CommentForm
from django.views.generic.edit import FormView

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile
# Create your views here.
def Dashboard(request):
    return render(request,'BlogApp/base.html')


# def signup(request):
#     if request.method == 'POST':
#         user_form = SignUpForm(request.POST)
#         profile_form = UserProfileForm(request.POST, request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
#
#             return redirect('login')  # Redirect to a success page
#
#     else:
#         user_form = SignUpForm()
#         profile_form = UserProfileForm()
#
#     return render(request, 'BlogApp/Sign_Up_Form.html', {'signupform': user_form, 'userprofileform': profile_form})
# from django.shortcuts import render, redirect
# from django.views import View
# from .forms import SignUpForm, UserProfileForm  # Assuming you have imported the necessary forms
#
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
            profile.user = user
            profile.save()
            return redirect('login')  # Redirect to a success page

        return render(request, self.template_name, {'signupform': user_form, 'userprofileform': profile_form})

def loginuser(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Dashboard')
            else:
                messages.error(request,"Invalid Authentication")
    else:
        form = LoginForm()

    return render(request, 'BlogApp/login.html', {'loginform': form})


def post(request):
    if request.method=="POST":
        form=UserPost(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user = request.user
            post.approved = False
            post.save()
            return redirect('Dashboard')
    else:
        form=UserPost()
    return render(request, 'BlogApp/Post.html', {'postform': form})




class UserPostListView(ListView):
    model = Post
    template_name = 'BlogApp/postlist.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Annotate each post with the count of likes
        queryset = super().get_queryset().annotate(like_count=Count('liked_by'))
        return queryset





class PostdetailView(DetailView):
    model = Post
    template_name = 'BlogApp/postdetail.html'
    context_object_name = 'posts'

def LikeView(request, pk):
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




@login_required
def approve_posts(request):
    if not UserProfile.objects.filter(user=request.user, role=UserProfile.UserRoleEnum.MODERATOR.value).exists():
        return redirect('Dashboard')

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
from .userprofileupdate import UserProfileUpdateForm

@login_required
def profile_update(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create a user profile if it doesn't exist yet
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_update')  # Redirect back to the profile update page
    else:
        form = UserProfileUpdateForm(instance=user_profile)

    return render(request, 'BlogApp/profile_update.html', {'userprofileupdate': form})




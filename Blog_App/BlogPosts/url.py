from django.urls import path
from . import views

urlpatterns = [
    path('',views.Dashboard,name='Dashboard'),
    path('register/',views.SignUpView.as_view(),name='Register'),
    path('login/',views.loginuser,name='login'),
    path('post/',views.post,name='post'),
    path('list/',views.UserPostListView.as_view(),name='list'),
    path('detail/<int:pk>/',views.PostdetailView.as_view(),name='detail'),
    path('like/<int:pk>/',views.LikeView,name='like'),
    path('post/<int:pk>/comments',views.AddComment.as_view(),name='add_comment'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/update/', views.update_post, name='update_post'),
    path('approve/', views.approve_posts, name='approve_posts'),
    path('profile/update/', views.profile_update, name='profile_update'),

]

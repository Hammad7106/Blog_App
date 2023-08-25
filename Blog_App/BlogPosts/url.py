from django.urls import path
from . import views

urlpatterns = [
    path('',views.Dashboard,name='Dashboard'),
    path('register/',views.SignUpView.as_view(),name='Register'),
    path('login/', views.Signin, name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('post/',views.CreatePostView.as_view(),name='post'),
    path('list/',views.UserPostListView.as_view(),name='list'),
    path('detail/<int:pk>/',views.PostdetailView.as_view(),name='detail'),
    path('like/<int:pk>/',views.LikeView.as_view(),name='like'),
    path('check_like/<int:post_id>/', views.CheckLikeView.as_view(), name='check_like'),
    path('post/<int:pk>/comments',views.AddComment.as_view(),name='add_comment'),
    path('comment/reply/<int:comment_id>/', views.reply_to_comment, name='reply_comment'),
    path('like_comment/<int:comment_id>/', views.CommentLikeView, name='like_comment'),
    path('check_comment_like/<int:comment_id>/', views.CheckCommentLikeView.as_view(), name='check_comment_like'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/update/', views.update_post, name='update_post'),
    path('approve/', views.approve_posts, name='approve_posts'),
    path('delete_unapproved_post/', views.delete_unapproved_post, name='delete_unapproved_post'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('report/<int:post_id>/', views.report_post, name='report_post'),
    path('moderator/', views.moderator_dashboard, name='moderator_dashboard'),
    path('delete/', views.delete_repo_post, name='delete'),

    path('list_suggestion/<int:post_id>/', views.suggestions_list, name='suggestions_list'),
    path('submit_suggestion/<int:post_id>/', views.submit_suggestion, name='submit_suggestion'),
    path('reply_suggestion/<int:suggestion_id>/', views.reply_suggestion, name='reply_suggestion'),
    path('delete_suggestion/<int:suggestion_id>/', views.delete_suggestion, name='delete_suggestion'),
    path('apply_suggestion/<int:suggestion_id>/', views.apply_suggestion, name='apply_suggestion'),


]

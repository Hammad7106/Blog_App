from django.urls import path
from . import views
from .views import add_comment,apply_suggestion,approve_post,check_post_likes\
    ,create_post,dashboard,delete_post,delete_repo_post,delete_suggestion,delete_unapproved_posts,\
    login,logout,moderator_dashboard,post_list,post_like,reply_comment,reply_suggestion,report_post,signup,\
    submit_suggestion,suggestion_list,update_post,update_profile,like_comments,report_comments,sending_mail

urlpatterns = [


    # SignUp, Login, Logout
    path('',post_list.UserPostListView.as_view(),name='Dashboard'),
    path('register/',signup.SignUpView.as_view(),name='Register'),
    path('login/',login.Signin, name='login'),
    path('logout/',logout.user_logout,name='logout'),



    # Profile Update
    path('profile/update/', update_profile.profile_update, name='profile_update'),
    path('mail/', sending_mail.mail, name='send_mail'),
    path('verify-email/<str:token>/', update_profile.verify_email_change, name='verify_email_change'),




    # URLS Related to POSTS
    path('post/',create_post.CreatePostView.as_view(),name='post'),
    path('list/',post_list.UserPostListView.as_view(),name='list'),
    path('like/<int:pk>/',post_like.LikeView.as_view(),name='like'),
    path('check_like/<int:post_id>/', check_post_likes.CheckLikeView.as_view(), name='check_like'),
    path('post/<int:pk>/comments',add_comment.AddComment.as_view(),name='add_comment'),
    path('posts/<int:post_id>/delete/',delete_post.delete_post, name='delete_post'),
    path('posts/<int:post_id>/update/', views.update_post.update_post, name='update_post'),
    path('report/<int:post_id>/', views.report_post.report_post, name='report_post'),



    # URLS Related to COMMENTS
    path('comment/reply/<int:comment_id>/',reply_comment.reply_to_comment, name='reply_comment'),
    path('comment/<int:comment_id>/like/', like_comments.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/unlike/',like_comments.unlike_comment, name='unlike_comment'),
    path('comment/<int:comment_id>/report/', report_comments.report_comment, name='report_comment'),
    path('comment/<int:comment_id>/unreport/', report_comments.unreport_comment, name='unreport_comment'),



    # URLS Related to MODERATOR ( Approve posts, delete posts, delete reported posts )
    path('approve/',approve_post.approve_posts, name='approve_posts'),
    path('delete_unapproved_post/', delete_unapproved_posts.delete_unapproved_post, name='delete_unapproved_post'),
    path('moderator/', views.moderator_dashboard.moderator_dashboard, name='moderator_dashboard'),
    path('delete/',delete_repo_post.delete_repo_post, name='delete'),




    # # URLS Related to SUGGESTIONS ( A user can submit suggestions to a post, Owner of post can check suggestions
    # in order to approve, reply or delete siggestion made by user )
    path('list_suggestion/<int:post_id>/', suggestion_list.suggestions_list, name='suggestions_list'),
    path('submit_suggestion/<int:post_id>/', submit_suggestion.SubmitSuggestionView.as_view(), name='submit_suggestion'),
    path('reply_suggestion/<int:suggestion_id>/', reply_suggestion.reply_suggestion, name='reply_suggestion'),
    path('delete_suggestion/<int:suggestion_id>/', delete_suggestion.delete_suggestion, name='delete_suggestion'),
    path('apply_suggestion/<int:suggestion_id>/', apply_suggestion.apply_suggestion, name='apply_suggestion'),

]




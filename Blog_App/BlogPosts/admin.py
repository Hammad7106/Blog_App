from django.contrib import admin
from .models import Post,Comments,Like,Report,Suggestion
# Register your models here.

from django.contrib import admin
from .models import  UserProfile,Post, Comments, Like, Report, Suggestion,CommentLike,SuggestionReply

@admin.register(UserProfile)
class BlogUser(admin.ModelAdmin):
    list_display = ('role','user','image')

@admin.register(Post)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_title', 'post_content','post_image','approved')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'description','attachment','parent_comment')


@admin.register(CommentLike)
class LikeComment(admin.ModelAdmin):
    list_display = ('user','comment')



@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('user','post','text','status')

@admin.register(SuggestionReply)
class ReplySuggestion(admin.ModelAdmin):
    list_display = ('suggestion','user','reply_text')

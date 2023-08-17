from django.contrib import admin
from .models import Post,Comments,Like,Report,Suggestion
# Register your models here.

from django.contrib import admin
from .models import  Post, Comments, Like, Report, Suggestion


@admin.register(Post)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('user','post_title', 'post_description','post_image')

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','post','description')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user','post','comment')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user','post','comment')

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('user','post','content','reply','status')


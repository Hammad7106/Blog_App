from django.contrib import admin
from .models import Post,Comments,Like,Report,Suggestion
# Register your models here.

from django.contrib import admin
from .models import  UserProfile,Post, Comments, Like, Report, Suggestion

@admin.register(UserProfile)
class BlogUser(admin.ModelAdmin):
    list_display = ('role','user','image')

@admin.register(Post)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_title', 'post_content','post_image','approved')

    # def get_likes_count(self, obj):
    #     return obj.liked_by.count()
    # get_likes_count.short_description = 'Likes'
    #
    # def get_reports_count(self, obj):
    #     return obj.reported_by.count()
    # get_reports_count.short_description = 'Reports'

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'description')

    def get_likes_count(self, obj):
        return obj.liked_by.count()
    get_likes_count.short_description = 'Likes'

    def get_reports_count(self, obj):
        return obj.reported_by.count()
    get_reports_count.short_description = 'Reports'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('user','post','content','reply','status')


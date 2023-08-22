from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from froala_editor.fields import FroalaField


# Create your models here.

class UserProfile(models.Model):
    class UserRoleEnum(Enum):
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        USER = 'user'

    role = models.CharField(max_length=20, choices=[(role.value, role.name) for role in UserRoleEnum],
                            default=UserRoleEnum.USER.value)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField(blank=True, null=True, upload_to='images/')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=20)
    # post_description=models.CharField(max_length=500)
    post_content = FroalaField(null=False)
    post_image = models.ImageField(blank=True, null=True, upload_to='images/')
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    reported_by = models.ManyToManyField(User, related_name='reported_posts', blank=True)
    approved=models.BooleanField(default=False)

    def __str__(self):
        return self.post_title


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_made')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    attachment = models.FileField(upload_to='', null=True, blank=True)
    liked_by = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    reported_by = models.ManyToManyField(User, related_name='reported_comments', blank=True)

    def __str__(self):
        return self.description


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_post')


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    reply = models.TextField(blank=True, null=True)
    status_choices = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

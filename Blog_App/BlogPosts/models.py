from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post_title=models.CharField(max_length=20)
    post_description=models.CharField(max_length=500)
    post_image=models.ImageField(blank=True,null=True,upload_to='images/')
    def __str__(self):
        return self.post_title

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments_made')
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    description=models.CharField(max_length=200)
    def __str__(self):
        return self.description

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='liked_post')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, blank=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True, blank=True)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True, blank=True)

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

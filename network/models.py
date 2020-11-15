from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="post_create") #if user is deleted, auction will be deleted
    
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    text = models.CharField(max_length=255, null=True)

    likes = models.IntegerField(default=None, null=True, blank=True)

    verify_like = models.BooleanField(default=True, null=True, blank=True)


class Followers(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user_follow")

    follower  =  models.ForeignKey(User, on_delete = models.CASCADE, related_name="follow_create")


class Like(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="like_user")

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name="like_post")



    


    


     

    
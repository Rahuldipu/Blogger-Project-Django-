from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class User_detail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.FileField(null=True)
    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50, null=True)
    sub_title = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)
    date = models.DateField(null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    userdetail = models.ForeignKey(User_detail, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.TextField(null=True)

    def __str__(self):
        return self.post.title

class Post_Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    like = models.IntegerField(null=True)

    def __str__(self):
        return self.post.title+"--"+str(self.like)

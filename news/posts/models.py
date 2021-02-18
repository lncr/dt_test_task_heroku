from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="posts", null=True
    )
    title = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    upvotes_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-id",)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="comments", null=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.email} - {self.creation_date}"

    class Meta:
        ordering = ("-id",)


class Upvote(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="upvotes")
    receiver = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="upvotes")

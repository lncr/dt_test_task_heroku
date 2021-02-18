from celery import shared_task

from .models import Post, Upvote


@shared_task
def reset_upvotes():

    upvotes = Upvote.objects.all()
    upvotes.delete()

    posts = Post.objects.all()
    posts.update(upvotes_amount=0)

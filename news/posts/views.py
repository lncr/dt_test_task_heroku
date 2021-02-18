from django.shortcuts import get_object_or_404
from rest_framework import views, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Comment, Post, Upvote
from .serializers import CommentSerializer, PostSerializer
from .permissions import IsAuthorOrReadOnly


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly, ]


class CommentModelViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly, ]

    def get_queryset(self):
        post_id = self.request.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        qs = Comment.objects.filter(post=post)
        return qs


class UpvotesAPIViw(views.APIView):

    permission_classes = [IsAuthenticated, ]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        upvote = Upvote.objects.filter(sender=user, receiver=post).first()

        if not upvote:
            Upvote.objects.create(sender=user, receiver=post)
            post.upvotes_amount += 1
            post.save(update_fields=['upvotes_amount'])
            return Response('You have upvoted the post')

        return Response('You have already upvoted this post today')

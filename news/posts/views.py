from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment, Post
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

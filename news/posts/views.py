from django.shortcuts import get_object_or_404
from rest_framework import views, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Comment, Post, Upvote
from .serializers import CommentSerializer, PostSerializer
from .permissions import IsAuthorOrReadOnly, IsPostAuthor


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"
    permission_classes = [
        IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly,
    ]


class CommentModelViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_field = "id"
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly | IsPostAuthor,
    ]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        qs = Comment.objects.filter(post=post)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        post = get_object_or_404(Post, id=kwargs["post_id"])

        if serializer.is_valid():
            comment = Comment.objects.create(
                author=request.user,
                content=serializer.validated_data["content"],
                post=post,
            )
            serializer = self.get_serializer(instance=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class UpvotesAPIViw(views.APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        upvote = Upvote.objects.filter(sender=user, receiver=post).first()

        if not upvote:
            Upvote.objects.create(sender=user, receiver=post)
            post.upvotes_amount += 1
            post.save(update_fields=["upvotes_amount"])
            return Response("You have upvoted the post")

        return Response("You have already upvoted this post today")

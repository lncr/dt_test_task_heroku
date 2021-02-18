from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostSerializer
from .permissions import ReadOnly


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated | ReadOnly, ]

from django.urls import path

from .views import CommentModelViewSet, PostModelViewSet, UpvotesAPIViw

list_params = {'get': 'list', 'post': 'create'}
detail_params = {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}

urlpatterns = [
    path('posts/', PostModelViewSet.as_view(list_params),
         name='posts_list_url'),
    path('posts/<int:id>/', PostModelViewSet.as_view(detail_params),
         name='post_detail_url'),
    path('posts/<int:post_id>/comments/', CommentModelViewSet.as_view(list_params),
         name='comments_list_url'),
    path('posts/<int:post_id>/comments/<int:id>/', CommentModelViewSet.as_view(detail_params),
         name='comment_detail_url'),
    path('posts/<int:post_id>/upvotes/', UpvotesAPIViw.as_view(), name='upvotes_url'),
]

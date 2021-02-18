from django.urls import path

from .views import PostModelViewSet

urlpatterns = [
    path('posts/', PostModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='posts_list_url'),
    path('posts/<int:id>/', PostModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='post_detail_url'),
]

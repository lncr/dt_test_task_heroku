from rest_framework import serializers

from .models import Post, Comment


class RepresentationMixIn:

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author_name'] = instance.author.username
        return representation


class PostSerializer(serializers.HyperlinkedModelSerializer, RepresentationMixIn):

    class Meta:
        fields = ['id', 'title', 'url', 'creation_date', 'upvotes_amount', ]
        read_only_fields = ['creation_date', 'upvotes_amount', ]

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        new_post = Post.objects.create(author=author, title=validated_data['title'])
        return new_post


class CommentSerializer(serializers.ModelSerializer, RepresentationMixIn):

    class Meta:
        fields = ['id', 'content', 'creation_date']
        read_only_fields = ['creation_date', ]

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        new_comment = Comment.objects.create(author=author, content=validated_data['content'])
        return new_comment

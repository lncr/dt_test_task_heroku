from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = ['id', 'title', 'url', 'creation_date', ]
        read_only_fields = ['creation_date', ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author_name'] = instance.author.username
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        new_post = Post.objects.create(author=author, title=validated_data['title'])
        return new_post

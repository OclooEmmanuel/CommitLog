from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'post', 'body', 'created_on', 'parent']
        read_only_fields = ['created_on']


class PostSerialiser(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'author_name', 'body', 'created_on', 'comments']
        read_only_fields = ['slug', 'created_on']  # Don't require these from user





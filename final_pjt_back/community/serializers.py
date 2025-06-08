from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)
    is_author = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'author_nickname', 'is_author']

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request and request.user.is_authenticated and obj.author == request.user

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField() 

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 
                 'comments', 'comment_count', 'author_nickname', 'is_author']

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request and request.user.is_authenticated and obj.author == request.user

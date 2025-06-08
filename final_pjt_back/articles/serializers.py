from rest_framework import serializers
from .models import Article

class ArticleListSerializer(serializers.ModelSerializer):
    article_type_display = serializers.CharField(source='get_article_type_display', read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'article_type',           # 내부 코드 (예: 'trend')
            'article_type_display',   # 사람이 읽기 쉬운 이름 (예: '경제·금융 트렌드')
            'created_at',
            'image',
        ]

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['id', 'author', 'content', 'created_at', 'approved']

class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'article_type', 'created_at', 'image']


class ArticleWriteSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Article
        fields = ['title', 'content', 'article_type', 'image']
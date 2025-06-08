from django.db import models
from markdownx.models import MarkdownxField

# Create your models here.
class Article(models.Model):
    TYPE_CHOICES = [
        ('strategy', '투자 전략/팁'),
        ('trend', '경제·금융 트렌드'),
        ('app', '금융 앱/서비스 소개'),
        ('glossary', '용어/상식 사전'),
    ]
    title = models.CharField(max_length=200)
    content = MarkdownxField()
    article_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True)


# class Comment(models.Model):
#     article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
#     author = models.CharField(max_length=100)
#     content = models.TextField(max_length=1000)
#     created_at = models.DateTimeField(auto_now_add=True)
#     approved = models.BooleanField(default=True)
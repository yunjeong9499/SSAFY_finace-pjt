from django.contrib import admin
from .models import Article
from markdownx.admin import MarkdownxModelAdmin

# admin.site.register(Article)
@admin.register(Article)
class ArticleAdmin(MarkdownxModelAdmin):
    list_display = ['title', 'article_type', 'created_at']


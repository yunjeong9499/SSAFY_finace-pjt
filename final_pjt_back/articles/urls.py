# urls.py
from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleCreateView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),  # /api/articles/
    path('<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),  # /api/articles/3/
    # path('<int:pk>/comments/', CommentListCreateView.as_view(), name='article-comments'),  # /api/articles/3/comments/
]
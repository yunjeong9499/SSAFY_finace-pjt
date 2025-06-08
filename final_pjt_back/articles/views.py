from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Article
from .serializers import ArticleListSerializer, ArticleDetailSerializer, ArticleWriteSerializer

class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleListSerializer

class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer

class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleWriteSerializer  # ✅ 위에서 만든 공용 serializer
    permission_classes = [IsAdminUser]

# class CommentListCreateView(generics.ListCreateAPIView):
#     serializer_class = CommentSerializer

#     def get_queryset(self):
#         article_id = self.kwargs['pk']
#         return Comment.objects.filter(article_id=article_id, approved=True)

#     def perform_create(self, serializer):
#         article_id = self.kwargs['pk']
#         serializer.save(article_id=article_id)
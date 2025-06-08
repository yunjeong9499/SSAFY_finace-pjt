from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

post_router = NestedDefaultRouter(router, 'posts', lookup='post')
post_router.register('comments', CommentViewSet, basename='post-comments')

urlpatterns = router.urls + post_router.urls

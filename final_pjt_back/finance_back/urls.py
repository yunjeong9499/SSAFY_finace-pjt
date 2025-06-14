"""
URL configuration for finance_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import CustomUserDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/signup/', include('dj_rest_auth.registration.urls')),  # ✅ 이거 필수!!
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/', include('products.urls')),
    path('api/community/', include('community.urls')),
    path('api/chat/', include('chatbot.urls')),    
    path('markdownx/', include('markdownx.urls')), 
    path('api/articles/', include('articles.urls')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

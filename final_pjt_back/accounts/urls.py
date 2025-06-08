# accounts/urls.py

from django.urls import path
from .views import UserSurveyView, UserProfileView, AccountDeleteView
from dj_rest_auth.views import PasswordChangeView
from .views import CustomUserDetailView, CustomRegisterView

urlpatterns = [
    path('signup/', CustomRegisterView.as_view(), name='custom_register'),
    path('user/', CustomUserDetailView.as_view(), name='custom-user-detail'),
    path('survey/', UserSurveyView.as_view(), name='user-survey'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('delete/', AccountDeleteView.as_view(), name='delete-user'), 
]

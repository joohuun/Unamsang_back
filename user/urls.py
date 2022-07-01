from django.contrib import admin
from django.urls import path
from user import views

from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.UserView.as_view()),
    path('login/', views.TokenObtainPairView.as_view(), name='sparta_token'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/authonly/', views.OnlyAuthenticatedUserView.as_view()),
    path('<obj_id>/', views.OnlyAuthenticatedUserView.as_view()),
]


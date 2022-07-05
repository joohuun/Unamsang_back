from django.urls import path, include
from . import views


# 뷰셋
from .views import CommentViewSet, RatingViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'rating', RatingViewSet, basename='rating') # (평점)
router.register(r'comment', CommentViewSet, basename='comment') # (댓글)



urlpatterns = [
    path('', views.ArticleView.as_view()),
    path('search/', views.ArticleSearchView.as_view(), name="search"),
    path('text/', views.ImageGenerationView.as_view()),
    path('', include(router.urls)),    
    path('<obj_id>/', views.ArticleView.as_view()),
]
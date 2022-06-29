from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleView.as_view()),
    path('search/', views.ArticleSearchView.as_view(), name="search"),
    path('<obj_id>/', views.ArticleView.as_view()),
]
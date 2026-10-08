from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.category_articles, name='category_articles'),
    path('article/<slug:slug>/like/', views.like_article, name='like_article'),
]
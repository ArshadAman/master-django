# drf_internals/urls.py
from django.urls import path
from .views import ArticleListView, CachedArticleView

urlpatterns = [
    path('articles.csv', ArticleListView.as_view(), name='article-list-csv'),
    path('articles/cached/', CachedArticleView.as_view(), name='article-list-cached'),
]
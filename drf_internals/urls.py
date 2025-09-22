# drf_internals/urls.py
from django.urls import path
from .views import ArticleListView, CachedArticleView, BadArticleListView, GoodArticleListView

urlpatterns = [
    path('articles.csv', ArticleListView.as_view(), name='article-list-csv'),
    path('articles/cached/', CachedArticleView.as_view(), name='article-list-cached'),
    path('articles/bad/', BadArticleListView.as_view(), name='bad-article-list'),
    path('articles/good/', GoodArticleListView.as_view(), name='good-article-list'),
]
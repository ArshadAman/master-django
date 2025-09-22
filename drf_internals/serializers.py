from rest_framework import serializers
from orm_internals.models import Author, Article

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class BadArticleSerializer(serializers.ModelSerializer):
    """An inefficent serializer that causes N+1 queries"""
    # Nesting this serializer will cause one query per article to fetch the author
    author = AuthorSerializer()

    # This field will cause another query per article
    tag_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'tag_count']
    
    def get_tag_count(self, obj):
        """This method runs one query for every article"""
        return obj.tags.count()
    
class GoodArticleSerializer(serializers.ModelSerializer):
    """An efficient serializer."""
    author = AuthorSerializer()

    # The value for this field will be supplied by annotation
    tag_count = serializers.IntegerField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'tag_count']
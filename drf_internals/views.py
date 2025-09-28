# drf_internals/views.py
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from .renderers import CSVRenderer
from orm_internals.models import Article
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class ArticleListView(APIView):
    """A View that list articles and supports csv rendering."""
    renderer_classes = [CSVRenderer] #Add our custom renderer

    def get(self, request, format=None):
        """
        Returns a list of all articles.
        """

        # For simplicity, we'are not using serializers yet
        articles_data = list(Article.objects.values('id', 'title','views'))
        return Response(articles_data)

class CachedArticleView(APIView):
    """
        A custom APIView that short-circuits the request if a cached response exits.
    """

    def dispatch(self, request, *args, **kwargs):
        "Define a unique cache key for this request"
        params = getattr(request, "query_params", None)
        qs = params.urlencode() if params is not None else request.GET.urlencode()
        cache_key = f"article_view_{request.path}_{qs}"

        # Try to get the response from the cache
        cached_response_data = cache.get(cache_key)
        
        if cached_response_data:
            print('Cache HIT! Short-circuiting with a cached response')
            drf_request = Request(request)
            renderer = JSONRenderer()
            response = Response(cached_response_data)
            response.accepted_renderer = renderer
            response.accepted_media_type = renderer.media_type
            response.renderer_context = {
                'request': drf_request,
                'response': response,
            }
            return response
        
        print("Cache MISS! Proceeding with the normal dispatch.")
        # If not in cache, proceed with the normal DRF dispatch
        response = super().dispatch(request, *args, **kwargs)

        # After the response is generated, cache it for future requests
        if response.status_code == 200:
            print('Caching the new response.')
            cache.set(cache_key, response.data, timeout=60)
        
        return response
    
    # Fetch the details only if it is not in the cache or if the cache has the timeout
    def get(self, request, format=None):
        article_data = list(Article.objects.values('id', 'title', 'views'))
        return Response(article_data)
    
# Day 19
from .serializers import BadArticleSerializer, GoodArticleSerializer
from rest_framework.generics import ListAPIView
from django.db.models import Count


class BadArticleListView(ListAPIView):
    """Uses the inefficient serializer, causing many queries"""
    queryset = Article.objects.all()
    serializer_class = BadArticleSerializer

class GoodArticleListView(ListAPIView):
    """Uses prefetching and annotations to be effiecient."""
    # By using select_related, prefetch_related, and annotate,
    # we provide all the data the serializer needs in one go
    queryset = Article.objects.select_related('author').annotate(
        tag_count = Count('tags')
    )
    serializer_class = GoodArticleSerializer


# Day 20
from rest_framework import viewsets

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """A simple viewset for viewing articles."""
    serializer_class = GoodArticleSerializer
    queryset = Article.objects.all() # We will overide this later


from .routers import versioned_dispatch
class VersionedArticleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GoodArticleSerializer
    
    def get_queryset(self):
        tenant_id = self.kwargs['tenant_id']
        print(f"Filtering for tenant: {tenant_id}")
        return Article.objects.select_related('author').annotate(
        tag_count = Count('tags')
    )

    @versioned_dispatch
    def versioned_list(self, request, *args, **kwargs):
        """V1 list method."""
        print("Running V1 of the list method.")
        return self.list(request, *args, **kwargs)

    def versioned_list_v2(self, request, *args, **kwargs):
        """V2 list method."""
        print("Running V2 of the list method.")
        return self.list(request, *args, **kwargs)
    


# Day 21:
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist() # Add the token to the denylist
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
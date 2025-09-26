from rest_framework.routers import DefaultRouter, Route

class TenantVersionRouter(DefaultRouter):
    """
    A custom router that prefixes routes with a tenant_id and dispatches to a different view method based on X-Api-Version header.
    """

    def get_routes(self, viewset):
        """Overrides get_routes to add custom dispathcing."""
        routes = super().get_routes(viewset)

        # Add a custom courte for versioned list views
        version_list_route = Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'versioned_list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix':'List'}
        )
        # We'll add our new route to the existing ones
        return [version_list_route] + routes
    
    def get_urls(self):
        """
        Overrides get_urls to wrap the default URLs with our tenant prefix.
        """
        # Get the standrad URLs geenrated by the present class
        default_urls = super().get_urls()

        # We don't have a real tenant model, so we'll just wrap the URL with a placeholder for the tenant_id

        from django.urls import path, include

        tenant_urls = [
            path('<str:tenant_id>/', include(default_urls))
        ]
        return tenant_urls
    
# We need a way to dispatch based on header. Let's patch our ViewSet
from functools import wraps

def versioned_dispatch(func):
    """A decorator to dispatch to a v1 or v2 method based on header"""
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        version = request.headers.get('X-Api-Version', '1')
        if version == '2':
            # Remap the function calll to a 'v2' version
            v2_func_name = func.__name__+ "_v2"
            v2_func = getattr(self, v2_func_name)
            return v2_func(request, *args, **kwargs)
        # Default to v1
        return func(self, request, *args, **kwargs)
    return wrapper



    
import re
from django.core.management.base import BaseCommand

MINI_URLS = [
    (r'^articles/(?P<year>[0-9]{4})/$', 'article-year-archive', 'articles/%s/'),
    (r'^articles/(?P<pk>[0-9]+)/$', 'article-detail', 'articles/%s/'),
    (r'^$', 'homepage', ''),
]

def mini_resolve(path):
    """A simplified version of Django's Resolve()"""
    for pattern, view_name, _ in MINI_URLS:
        match = re.search(pattern, path)
        if match:
            kwargs = match.groupdict()
            print(f"✅ Path '{path}' resolved to '{view_name}' with args: {kwargs}")
            return view_name, kwargs
        print(f"❌ Path '{path}' did not resolve.")
        return None, {}

def mini_reverse(view_name, *args):
    """A simplified Django Reverse"""
    for _, name, url_format in MINI_URLS:
        if name == view_name:
            # Build the url by filling in the arguments
            url = url_format % args
            print(f"✅ View '{view_name}' reversed to '/{url}'")
            return f"/{url}"
    print(f"❌ View '{view_name}' could not be reversed.")
    return None    

class Command(BaseCommand):
    help = 'Runs a mini Url Resolver and reverse function'

    def handle(self, *args, **options):
        print("--- Testing mini resolve ---")
        mini_resolve('articles/2025/')
        mini_resolve('articles/123/')
        mini_resolve('about/')

        print("--- Testing mini reverse ---")
        mini_reverse('article-year-archive', '2024')
        mini_reverse('article-detail', 456)
        
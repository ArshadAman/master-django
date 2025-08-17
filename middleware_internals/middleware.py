import time
from django.http import HttpResponseForbidden, HttpResponse

# Middleware 1: Request Timing
class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Code on the way IN (before view)
        request.start_time = time.time()
        response = self.get_response(request)
        # Code on the way Out (after view)
        duration = time.time() - request.start_time
        response['X-Request-Time-ms'] = str(round(duration*1000, 2))
        print(f"Request to {request.path} took {duration:.2f}s")

        return response
    
# Middleware 2: "Early Exit" Authentication
class SimpleAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for a special header. For admin paths, let them pass.
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        
        if request.headers.get('X-API-Key') != 'my-secret-key':
            print('Auth Failed: No/Wrong api key. Short-circuiting.')
            # Short-circuit: Return a response immediatly
            return HttpResponseForbidden("Missing or Invalid API Key")

        print("Auth Passed")
        return self.get_response(request)
        
# MIddleware 3: Simple header Adder
class RateLimitHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-RateLimit-Remaining'] = '100' # Dummy value
        print("Added rate limit header.")
        return response


import time
from django.urls import resolve

class LifecycleLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("--- Middleware initialized ---")

    def __call__(self, request):
        # code to be executed for each request before the view is called
        request.start_time = time.time()
        print(f"\n[{request.start_time:.4f}] Middleware: Request received")
        print(f"-> Headers: {request.headers.get('Accept')}")

        # Resolve the url just before the view
        resolved_url = resolve(request.path_info)
        print(f"-> Url Resolved to: {resolved_url.view_name}")

        print("--- Middleware: Entering View ---")
        response = self.get_response(request)
        print("--- Middleware: Exited View ---")

        # code to be executed for each request/response after the view is called
        duration = time.time() - request.start_time
        print(f"[{time.time():.4f}] Middleware: Response ready (took {duration: .4f})s")

        # Check if the response is streaming
        if hasattr(response, 'streaming') and response.streaming:
            print("-> Response is streaming")
        else:
            print("-> Response is not streaming")
        return response
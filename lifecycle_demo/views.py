from django.http import HttpResponse
import time

def home_view(request):
    print("--- View: Start ---")
    time.sleep(1)
    response = HttpResponse("Hello from the home view")
    print("--- View: Finish ---")
    return response
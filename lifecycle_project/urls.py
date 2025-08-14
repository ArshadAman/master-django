from django.contrib import admin
from django.urls import path, include
from lifecycle_demo.views import home_view
from django.urls import resolve
import timeit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('view/', include('view_internals.urls')),
]

for i in range(5000):
    urlpatterns.append(
        path(f'test/route/number/{i}/', home_view, name=f'test-route-{i}')
    )

# A simple view to test the resolver
def test_resolver_speed(request):
    # We resolve one of the last URLs to measure the worst-case time
    path_to_resolve = '/test/route/number/4999/'
    
    # Use timeit to run resolve() many times for an accurate measurement
    number_of_runs = 10000
    total_time = timeit.timeit(lambda: resolve(path_to_resolve), number=number_of_runs)
    
    avg_time_micros = (total_time / number_of_runs) * 1_000_000
    print(f"Average resolve time over {number_of_runs} runs: {avg_time_micros:.2f} microseconds.")
    
    return home_view(request)

urlpatterns.append(path('test-speed/', test_resolver_speed))
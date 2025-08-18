from django.urls import path
from .views import stream_csv_view

urlpatterns = [
    path('stream/', stream_csv_view, name='stream-csv'),
]
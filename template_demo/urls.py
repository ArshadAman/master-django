from django.urls import path
from .views import template_test_view

urlpatterns = [
    path('', template_test_view, name='template_test_view')
]

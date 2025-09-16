from django.urls import path
from .views import product_form_view

urlpatterns = [
    path('demo', product_form_view, name='product_form')
]

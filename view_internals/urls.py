from django.urls import path
from .mini_cbv import MyTestView

urlpatterns = [
    path('test/', MyTestView.as_view(), name='test-view'),
]

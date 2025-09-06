# signals_demo/models.py
from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
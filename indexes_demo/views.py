from django.shortcuts import render
import random
from .models import Product
# Create your views here.
brands = ["TechCorp", "Clicker", "GigaWare", "NanoGear"]
for i in range(200):
  brand = random.choice(brands)
  Product.objects.create(
    name=f"Device {i}",
    metadata={"brand": brand, "specs": {"id": i}}
  )
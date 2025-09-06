# signals_demo/services.py
from .models import Product, AuditLog

def create_product_with_audit(name, price):
    """
    A service function that creates a product and explicitly logs it.
    """
    product = Product.objects.create(name=name, price=price)
    AuditLog.objects.create(
        message=f"Product '{product.name}' was created via service."
    )
    print("SERVICE CALLED: Explicitly logged product creation.")
    return product
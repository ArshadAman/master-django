# signals_demo/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, AuditLog

@receiver(post_save, sender=Product)
def log_product_change(sender, instance, created, **kwargs):
    """
    A receiver function that logs when a Product is created or saved.
    """
    action = "created" if created else "updated"
    AuditLog.objects.create(
        message=f"Product '{instance.name}' was {action}."
    )
    print(f"SIGNAL FIRED: Product '{instance.name}' was {action}.")
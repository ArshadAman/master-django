# indexes_demo/models.py
from django.db import models
from django.contrib.postgres.indexes import GinIndex

class Product(models.Model):
    name = models.CharField(max_length=100)
    # A JSONB field to store unstructured metadata
    metadata = models.JSONField()

    class Meta:
        indexes = [
            # Create a GIN index on the metadata field
            GinIndex(fields=['metadata'], name='product_metadata_gin_idx'),
        ]
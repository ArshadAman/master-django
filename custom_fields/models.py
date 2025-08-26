from django.db import models
from .fields import EncryptedTextField
# Create your models here.
class SecretNote(models.Model):
    title = models.CharField(max_length=30)
    secret_content = EncryptedTextField()

    def __str__(self):
        return self.title


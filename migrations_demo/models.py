from django.db import models

class Profile(models.Model):
    # full_name = models.CharField(max_length=100) Remove this after running RunPython
    # Add new fields, allowing them to be null for now
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    
    def __str__(self):
        return self.full_name

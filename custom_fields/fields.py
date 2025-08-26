from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet
from django.core.exceptions import ImproperlyConfigured

# print(Fernet.generate_key()) : generate the key and store it safely in the env or secure vault

if not hasattr(settings, 'FERNET_KEY'):
    raise ImproperlyConfigured("FERNET_KEY is improperly configured")

fernet = Fernet(settings.FERNET_KEY)

class EncryptedTextField(models.TextField):
    """A custom fields that encrypts and decrypts the data"""

    def from_db_value(self, value, expression, connection):
        """Decrypts the data from the database"""
        if value is None:
            return value
        try:
            # The value of db is string, needs to be in bytes
            return fernet.decrypt(value.encode('utf-8')).decode('utf-8')
        except Exception:
            return value #if decryption fails return the value
    
    def to_python(self, value):
        """Converts the value to a Python object (string)."""
        # This is called during deserialization and from form fields.
        # If it's already a string, we don't need to do anything.
        if isinstance(value, str):
            return value
        if value is None:
            return value
        # from db value handles the encryption
        return str(value)
    
    def get_prep_value(self, value):
        """Encrypts the value before saving it to the database"""
        if value is None:
            return value
        # Encrypts the string and get the bytes
        encrypted_bytes = fernet.encrypt(str(value).encode('utf-8'))
        # Return as string to be stored in the text fields

        return encrypted_bytes.decode('utf-8')
    
    def deconstruct(self):
        """Allows migrations to serialize the field"""
        name, path, args, kwargs = super().deconstruct()
        # No custom arguments to add for this simple field
        return name, path, args, kwargs
    
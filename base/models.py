from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add your custom fields here
    tenant_id = models.CharField(max_length=5000, blank=True, null=True)
    user_type= models.CharField(max_length=100, blank=True, null=True)
    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    # Add your custom fields here
    user_uuid = models.CharField(max_length=100, blank=True, null=True)
    tenant_id = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    user_type= models.CharField(max_length=100, blank=True, null=True)
    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
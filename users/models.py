from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    # барои ҳал кардани clash бо auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # default 'user_set' clash мекунад
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set_permissions',  # default clash
        blank=True,
        help_text='Specific permissions for this user.'
    )

    REQUIRED_FIELDS = ['phone_number']

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    is_coordinator = models.BooleanField(default=False)
    is_planner = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Custom related name to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Custom related name to avoid conflict
        blank=True
    )

    def __str__(self):
        return self.username

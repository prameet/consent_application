from django.db import models
from accounts.models import CustomUser
import uuid
class PlannerService(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_code = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.service_code:
            self.service_code = f"PLANNER-{uuid.uuid4().hex[:8]}"  # Generates unique ID
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.user.username} - {self.service_code}"

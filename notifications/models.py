from django.db import models
from accounts.models import Employee

class Notification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.message[:20]}"

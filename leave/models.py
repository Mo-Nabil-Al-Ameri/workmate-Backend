from django.db import models
from accounts.models import Employee

class LeaveType(models.TextChoices):
    ANNUAL = "Annual Leave"
    SICK = "Sick Leave"
    EMERGENCY = "Emergency Leave"

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, default="Pending", choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")])

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type} ({self.start_date} - {self.end_date})"

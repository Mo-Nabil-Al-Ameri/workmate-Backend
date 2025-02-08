from django.db import models
from accounts.models import Employee

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance_records")
    check_in = models.DateTimeField(auto_now_add=True)  # وقت الحضور
    check_out = models.DateTimeField(null=True, blank=True)  # وقت الانصراف

    def __str__(self):
        return f"{self.employee.name} - {self.check_in.strftime('%Y-%m-%d %H:%M')}"

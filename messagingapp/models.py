from django.db import models
from accounts.models import Employee

class Message(models.Model):
    sender = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.name} to {self.receiver.name}: {self.subject}"

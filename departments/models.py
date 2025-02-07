from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()

class Department(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    manager = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_department'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:  # توليد `id` تلقائي إذا لم يتم تحديده
            last_id = Department.objects.aggregate(models.Max('id'))['id__max'] or 0
            next_id = last_id + 1
            if next_id > 99:  # حد أقصى
                raise ValueError("ID exceeded the allowed maximum value of 99.")
            self.id = next_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id:02} - {self.name}"

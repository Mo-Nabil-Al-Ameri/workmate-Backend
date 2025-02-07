from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=100, unique=True)  # اسم الوظيفة
    description = models.TextField(null=True, blank=True)  # وصف الوظيفة
    default_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # الراتب الافتراضي

    def __str__(self):
        return self.title

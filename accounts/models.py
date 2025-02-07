from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from datetime import datetime

class Roles(models.TextChoices):
    Emp ='Employee'
    HRM='HR Manager'
    Admin='Admin'
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    Gender_CHOICES = (
            ('Male', 'Male'),
            ('Female', 'Female'),
        )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,null=True, unique=True)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.Emp)
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()
    gender = models.CharField(max_length=10, choices=Gender_CHOICES, null=True, blank=True)    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

class Employee(User):
    job = models.ForeignKey('jobs.Job',on_delete=models.SET_NULL,null=True,blank=True,related_name="Employees")
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE,related_name='department_members')

    # بيانات شخصية
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=10, choices=[('Single', 'Single'), ('Married', 'Married')], null=True, blank=True)

    # بيانات الاتصال
    address = models.TextField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=20, null=True, blank=True)

    # بيانات وظيفية
    employee_number = models.CharField(max_length=10, unique=True, editable=False,default=None)
    employment_type = models.CharField(max_length=20, choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time')])
    contract_type = models.CharField(max_length=20, choices=[('Permanent', 'Permanent'), ('Temporary', 'Temporary'), ('Freelance', 'Freelance')],null=True,blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    disciplinary_record = models.TextField(null=True, blank=True)
    training_record = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.employee_number:
            self.employee_number = self.generate_employee_number()
        super().save(*args, **kwargs)

    def generate_employee_number(self):
        year = datetime.now().year  # السنة بأربعة أرقام
        department = self.department  # قسم الموظف
        department_code = str(department.id).zfill(2) if department else "00"
        
        # استعلام للحصول على آخر رقم تسلسلي
        last_employee = (
            Employee.objects.filter(department=department)
            .order_by('employee_number')
            .last()
        )
        last_sequence = (
            int(last_employee.employee_number[-3:]) if last_employee and last_employee.employee_number else 0
        )
        sequence = str(last_sequence + 1).zfill(3)

        return f"{year}{department_code}{sequence}"

    
    def __str__(self):
        return f"{self.name}{self.email}"

class Profile(models.Model):
    employee = models.OneToOneField('Employee', on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)  # نبذة شخصية
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    # social_links = models.JSONField(null=True, blank=True)  # روابط اجتماعية إضافية
    def __str__(self):
        return f"Profile of {self.employee.name}"

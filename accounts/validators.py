import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

def set_default_salary(job):
    """
    تعيين الراتب الافتراضي بناءً على الوظيفة، أو 0 إذا لم يكن هناك راتب افتراضي.
    """
    if job and hasattr(job, 'default_salary'):
        return job.default_salary
    return 0  # قيمة افتراضية عند عدم وجود وظيفة أو راتب

# التحقق من الاسم الرباعي
def validate_full_name(value):
    if len(value.split()) < 4:
        raise ValidationError("The name must include at least four parts (first name, middle names, and last name).")

# التحقق من البريد الإلكتروني
def validate_email(value):
    email_validator = EmailValidator()
    email_validator(value)  # التحقق باستخدام مكتبة Django

# التحقق من رقم الهاتف
def validate_phone(value):
    pattern = r'^\+?\d{10,15}$'  # رقم هاتف بصيغة +1234567890 أو 1234567890
    if not re.match(pattern, value):
        raise ValidationError("Invalid phone number format. Use +1234567890 or 1234567890.")

# التحقق من كلمة المرور
def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', value):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', value):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', value):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r'[!@#$%^&*()-_,.?":{}|<>]', value):
        raise ValidationError("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")

# # تحديد راتب الموظف بناءً على الوظيفة
# def set_default_salary(instance):
#     if not instance.salary and instance.job:
#         instance.salary = instance.job.default_salary  # تأكد من أن لديك حقل `default_salary` في نموذج `Job`

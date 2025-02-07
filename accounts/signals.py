from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee,Profile
from .utils import send_verification_email

@receiver(post_save, sender=Employee)
def send_email_verification(sender, instance, created, **kwargs):
    """إرسال بريد التحقق بعد إنشاء المستخدم"""
    if created:
        print(f"📧 Sending email to {instance.email}")  # ✅ تأكيد تشغيل الإشارة        
        send_verification_email(instance)

@receiver(post_save, sender=Employee)
def create_employee_profile(sender, instance, created, **kwargs):
    """
    يتم إنشاء `Profile` لكل موظف جديد تلقائيًا عند إنشاء الحساب.
    """
    if created:  # يتم تنفيذ الكود فقط عند إنشاء موظف جديد
        Profile.objects.create(employee=instance)

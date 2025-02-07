from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from itsdangerous import URLSafeTimedSerializer

# ✅ إنشاء التوكن
def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt='email-confirmation')

# ✅ التحقق من صحة التوكن
def verify_token(token, expiration=3600):  # 1 ساعة صلاحية
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt='email-confirmation', max_age=expiration)
    except Exception:
        return None
    return email

# ✅ إرسال البريد الإلكتروني مع رابط التحقق
def send_verification_email(user):
    token = generate_verification_token(user.email)
    verification_url = f"http://127.0.0.1:8000/api/v1/accounts/verify-email/{token}/"

    subject = "تفعيل حسابك في الموقع"
    message = f"مرحبًا {user.name},\n\nالرجاء النقر على الرابط التالي لتفعيل حسابك:\n\n{verification_url}\n\nإذا لم تقم بالتسجيل، يمكنك تجاهل هذه الرسالة."

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

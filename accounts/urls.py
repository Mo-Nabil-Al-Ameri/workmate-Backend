from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, EmployeeViewSet, UpdateProfileView, verify_email, login_user,register_user  

# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')
# router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('register/', register_user, name='register'),  # ✅ إضافة رابط تسجيل الحساب

    path('login/', login_user, name='login'),

    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),

    path('verify-email/<str:token>/', verify_email, name='verify-email'),

]

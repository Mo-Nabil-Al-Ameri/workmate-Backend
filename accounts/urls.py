from django.urls import path,include
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),

    # Profile
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('update/', views.UserUpdateAPIView.as_view(), name='update'),
    path('users/', views.GetAllEmployeesView.as_view(), name='users-list'),

    # Password Management
    path('change-password/', views.ChangePasswordAPIView.as_view(), name='change_password'),
    path('password-reset/', include('django_rest_passwordreset.urls'), name='password reset'),
    path('password-reset/confirm/', views.PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
    path('password-reset/validate_token/', views.PasswordResetValidateTokenAPIView.as_view(), name='password_reset_validate'),

    # OTP and Verification
    path('otp-send/', views.OTPSendAPIView.as_view(), name='otp_send'),
    path('otp-verify/', views.OTPVerifyAPIView.as_view(), name='otp_verify'),
    path('token/verify/', views.TokenVerifyAPIView.as_view(), name='token_verify'),
    path('token/refresh/', views.TokenRefreshAPIView.as_view(), name='token_refresh'),

    # Third-party Integration
    # path('google/login/', views.GoogleLoginAPIView.as_view(), name='google_login'),
]

# from django.urls import path, include
# from .views import UserViewSet, EmployeeViewSet, UpdateProfileView, verify_email, login_user,register_user  

# # router = DefaultRouter()
# # router.register(r'users', UserViewSet, basename='user')
# # router.register(r'employees', EmployeeViewSet, basename='employee')

# urlpatterns = [
#     path('register/', register_user, name='register'),  # ✅ إضافة رابط تسجيل الحساب

#     path('login/', login_user, name='login'),

#     path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),

#     path('verify-email/<str:token>/', verify_email, name='verify-email'),

# ]

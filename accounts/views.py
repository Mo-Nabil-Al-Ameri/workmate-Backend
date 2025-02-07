from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import( 
    UserSerializer,EmployeeSerializer,
    UserChangePasswordSerializer,
    UserUpdateSerializer,
    EmployeeOutputSerializer)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Accounts'])
class RegisterAPIView(APIView):
    serializer_class = EmployeeSerializer
    permission_classes=[]
    authentication_classes=[]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response({
                "message": "تم تسجيل الموظف بنجاح! يرجى التحقق من بريدك الإلكتروني لتفعيل الحساب.",
                "employee_number": employee.employee_number,
                "employee_email": employee.email,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Accounts'])
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
@extend_schema(tags=['Accounts'])
class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        employee = Employee.objects.filter(email=email).first()

        if not employee or not employee.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(employee)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Login successful!"
        })

# class LoginAPIView(APIView):
#     permission_classes = []

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(request, email=email, password=password)

#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#                 "message": "Login successful!"
#             })
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.generics import RetrieveAPIView
from .serializers import ProfileSerializer
@extend_schema(tags=['Accounts'])
class ProfileAPIView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = EmployeeOutputSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# class ProfileAPIView(RetrieveAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user.profile


from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import EmployeeSerializer
from .services import user_update
@extend_schema(tags=['Accounts'])
class UserUpdateAPIView(UpdateAPIView):
    """
    يسمح للموظف العادي فقط بتحديث بياناته الشخصية والملف الشخصي
    """
    serializer_class = UserUpdateSerializer
    permission_classes = []

    def get_object(self):
        return self.request.user  # الموظف الحالي فقط

# class UserUpdateAPI(APIView):
#     serializer_class = EmployeeSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def put(self, request):
#         """
#         Update the authenticated employee's profile information.
#         """
#         user = request.user
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             # Call the service function for updating the user
#             user_update(
#                 user=user,
#                 name=serializer.validated_data.get('name', None),
#                 email=serializer.validated_data.get('email', None),
#                 phone=serializer.validated_data.get('phone', None),
#                 role=serializer.validated_data.get('role', None),
#                 salary=serializer.validated_data.get('salary', None),
#                 department=serializer.validated_data.get('department', None),
#                 job=serializer.validated_data.get('job', None),
#                 address=serializer.validated_data.get('address', None),
#                 emergency_contact=serializer.validated_data.get('emergency_contact', None),
#                 date_of_birth=serializer.validated_data.get('date_of_birth', None),
#                 marital_status=serializer.validated_data.get('marital_status', None)
#             )
#             return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class UpdateAPIView(UpdateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user

@extend_schema(tags=['Accounts'])
class ChangePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class=UserChangePasswordSerializer
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)

from rest_framework_simplejwt.views import TokenRefreshView
@extend_schema(tags=['Accounts'])
class TokenRefreshAPIView(TokenRefreshView):
    """
    تحديث الـ Access Token باستخدام الـ Refresh Token.
    """
    pass
@extend_schema(tags=['Accounts'])
class PasswordResetValidateTokenAPIView(APIView):
    permission_classes = []  # مفتوح للجميع

    def post(self, request):
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')

        try:
            # فك ترميز UID
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            # تحقق من التوكن باستخدام PasswordResetTokenGenerator
            if PasswordResetTokenGenerator().check_token(user, token):
                return Response({"message": "Token is valid."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework_simplejwt.views import TokenVerifyView
@extend_schema(tags=['Accounts'])
class TokenVerifyAPIView(TokenVerifyView):
    """
    التحقق من صلاحية الـ Access Token.
    """
    pass
@extend_schema(tags=['Accounts'])
class PasswordResetConfirmAPIView(APIView):
    permission_classes = []

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        user = validate_reset_token(token)  # تحقق من التوكن
        if user:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Accounts'])
class OTPSendAPIView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = generate_otp(user)  # وظيفة لتوليد OTP
            send_otp_email(user, otp)  # وظيفة لإرسال الإيميل
            return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)
        return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
@extend_schema(tags=['Accounts'])
class PasswordResetAPIView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            send_password_reset_email(user)  # وظيفة لإرسال الإيميل
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
@extend_schema(tags=['Accounts'])
class OTPVerifyAPIView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user = User.objects.filter(email=email).first()
        if user and verify_otp(user, otp):  # تحقق من OTP
            return Response({"message": "OTP verified successfully!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.viewsets import ModelViewSet
# from .models import User, Employee, Profile
# from .serializers import UserSerializer, EmployeeSerializer, ProfileSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from .utils import verify_token,send_verification_email


# # ✅ تأكيد البريد الإلكتروني
# @api_view(['GET'])
# @permission_classes([AllowAny])  # يمكن لأي شخص فتح رابط التحقق
# def verify_email(request, token):
#     email = verify_token(token)
#     if email is None:
#         return Response({'error': 'رابط التحقق غير صالح أو منتهي الصلاحية'}, status=400)

#     try:
#         user = User.objects.get(email=email)
#         if user.is_active:
#             return Response({'message': 'تم تفعيل الحساب بالفعل!'}, status=200)
#         user.is_active = True
#         user.save()
#         return Response({'message': 'تم تفعيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.'}, status=200)
#     except User.DoesNotExist:
#         return Response({'error': 'المستخدم غير موجود'}, status=404)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     serializer = UserSerializer(data=request.data)

#     if serializer.is_valid():
#         user = serializer.save()
#         user.is_active = False  # الحساب غير مفعل حتى يتم التحقق من البريد
#         user.save()

#         # ✅ إرسال بريد التحقق بعد التسجيل
#         send_verification_email(user)

#         return Response({'message': 'تم إنشاء الحساب بنجاح! يرجى التحقق من بريدك الإلكتروني لتفعيله.'}, status=status.HTTP_201_CREATED)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @permission_classes([AllowAny])  # السماح لأي شخص بالوصول إلى رابط التحقق
# def verify_email(request, token):
#     email = verify_token(token)
#     if email is None:
#         return Response({'error': 'رابط التحقق غير صالح أو منتهي الصلاحية'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.get(email=email)
#         if user.is_active:
#             return Response({'message': 'تم تفعيل الحساب بالفعل!'}, status=status.HTTP_200_OK)

#         user.is_active = True
#         user.save()
#         return Response({'message': 'تم تفعيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.'}, status=status.HTTP_200_OK)
    
#     except User.DoesNotExist:
#         return Response({'error': 'المستخدم غير موجود'}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['POST'])
# @permission_classes([AllowAny])  # السماح للجميع بمحاولة تسجيل الدخول
# def login_user(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     user = authenticate(request, username=email, password=password)

#     if user is None:
#         return Response({'error': 'بيانات تسجيل الدخول غير صحيحة'}, status=400)

#     if not user.is_active:
#         return Response({'error': 'يجب تفعيل الحساب عبر البريد الإلكتروني قبل تسجيل الدخول'}, status=403)

#     refresh = RefreshToken.for_user(user)
#     return Response({
#         'access': str(refresh.access_token),
#         'refresh': str(refresh)
#     })

# # ✅ تحديث الملف الشخصي
# class UpdateProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request):
#         try:
#             profile = Profile.objects.get(employee=request.user)
#         except Profile.DoesNotExist:
#             return Response({"error": "الملف الشخصي غير موجود."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = ProfileSerializer(profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ✅ إدارة المستخدمين (CRUD)
# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     # السماح للجميع بإنشاء مستخدم، لكن التعديل والحذف يتطلب تسجيل الدخول
#     def get_permissions(self):
#         if self.action == "create":
#             return [AllowAny()]
#         return [IsAuthenticated()]


# # ✅ إدارة الموظفين (CRUD)
from rest_framework.viewsets import ModelViewSet
from .models import Employee
class EmployeeViewSet(APIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]  # السماح لأي شخص بإنشاء حساب جديد
        return [IsAuthenticated()]  # باقي العمليات تتطلب تسجيل الدخول    
      #  يجب أن يكون المستخدم مسجلاً للدخول

class GetAllEmployeesView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

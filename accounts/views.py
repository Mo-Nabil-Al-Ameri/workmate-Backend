from rest_framework.viewsets import ModelViewSet
from .models import User, Employee, Profile
from .serializers import UserSerializer, EmployeeSerializer, ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import verify_token,send_verification_email


# ✅ تأكيد البريد الإلكتروني
@api_view(['GET'])
@permission_classes([AllowAny])  # يمكن لأي شخص فتح رابط التحقق
def verify_email(request, token):
    email = verify_token(token)
    if email is None:
        return Response({'error': 'رابط التحقق غير صالح أو منتهي الصلاحية'}, status=400)

    try:
        user = User.objects.get(email=email)
        if user.is_active:
            return Response({'message': 'تم تفعيل الحساب بالفعل!'}, status=200)
        user.is_active = True
        user.save()
        return Response({'message': 'تم تفعيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'المستخدم غير موجود'}, status=404)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False  # الحساب غير مفعل حتى يتم التحقق من البريد
        user.save()

        # ✅ إرسال بريد التحقق بعد التسجيل
        send_verification_email(user)

        return Response({'message': 'تم إنشاء الحساب بنجاح! يرجى التحقق من بريدك الإلكتروني لتفعيله.'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])  # السماح لأي شخص بالوصول إلى رابط التحقق
def verify_email(request, token):
    email = verify_token(token)
    if email is None:
        return Response({'error': 'رابط التحقق غير صالح أو منتهي الصلاحية'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        if user.is_active:
            return Response({'message': 'تم تفعيل الحساب بالفعل!'}, status=status.HTTP_200_OK)

        user.is_active = True
        user.save()
        return Response({'message': 'تم تفعيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.'}, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response({'error': 'المستخدم غير موجود'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])  # السماح للجميع بمحاولة تسجيل الدخول
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, username=email, password=password)

    if user is None:
        return Response({'error': 'بيانات تسجيل الدخول غير صحيحة'}, status=400)

    if not user.is_active:
        return Response({'error': 'يجب تفعيل الحساب عبر البريد الإلكتروني قبل تسجيل الدخول'}, status=403)

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    })

# ✅ تحديث الملف الشخصي
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            profile = Profile.objects.get(employee=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "الملف الشخصي غير موجود."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ إدارة المستخدمين (CRUD)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # السماح للجميع بإنشاء مستخدم، لكن التعديل والحذف يتطلب تسجيل الدخول
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]


# ✅ إدارة الموظفين (CRUD)
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]  # السماح لأي شخص بإنشاء حساب جديد
        return [IsAuthenticated()]  # باقي العمليات تتطلب تسجيل الدخول
      # يجب أن يكون المستخدم مسجلاً للدخول

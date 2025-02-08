from rest_framework import viewsets
from .models import Department
from .serializers import DepartmentSerializer
from accounts.permissions import IsAdminOrHRM
from drf_spectacular.utils import extend_schema
@extend_schema(tags=['Departments'])
class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API لعرض وإنشاء وتحديث وحذف الأقسام، متاحة فقط لـ `Admin` و `HRM`.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrHRM]

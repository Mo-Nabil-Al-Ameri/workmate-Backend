from rest_framework import viewsets
from .models import Job
from .serializers import JobSerializer
from accounts.permissions import IsAdminOrHRM
from drf_spectacular.utils import extend_schema
@extend_schema(tags=['Jobs'])
class JobViewSet(viewsets.ModelViewSet):
    """
    API لعرض وإنشاء وتحديث وحذف الوظائف، متاحة فقط لـ `Admin` و `HRM`.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdminOrHRM]

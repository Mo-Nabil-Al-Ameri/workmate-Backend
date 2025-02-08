from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer
from drf_spectacular.utils import extend_schema
@extend_schema(tags=["Attendants"])
class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API لإدارة الحضور والانصراف.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

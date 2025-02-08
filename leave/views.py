from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Leaves"])
class LeaveRequestViewSet(viewsets.ModelViewSet):
    """
    API لإدارة طلبات الإجازات.
    """
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Notifications"])
class NotificationViewSet(viewsets.ModelViewSet):
    """
    API لإدارة الإشعارات.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

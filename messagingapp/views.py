from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Messages"])
class MessageViewSet(viewsets.ModelViewSet):
    """
    API لإدارة الرسائل بين الموظفين.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

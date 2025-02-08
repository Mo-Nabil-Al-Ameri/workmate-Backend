from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from drf_spectacular.utils import extend_schema
@extend_schema(tags=["Tasks"])
class TaskViewSet(viewsets.ModelViewSet):
    """
    API لإدارة المهام.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

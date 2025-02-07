from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    """
    Serializer لوظيفة معينة
    """

    class Meta:
        model = Job
        fields = "__all__"  # ✅ تضمين جميع الحقول

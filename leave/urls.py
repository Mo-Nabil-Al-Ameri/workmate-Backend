from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveRequestViewSet

router = DefaultRouter()
router.register(r'', LeaveRequestViewSet)

urlpatterns = router.urls

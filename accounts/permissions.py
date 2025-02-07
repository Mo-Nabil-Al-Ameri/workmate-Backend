from rest_framework.permissions import BasePermission

class IsAdminOrHRM(BasePermission):
    """
    يسمح فقط للمسؤول (Admin) أو مدير الموارد البشرية (HRM) بتنفيذ العمليات.
    """

    def has_permission(self, request, view):
        # السماح فقط إذا كان المستخدم مسجلاً ولديه الصلاحيات المطلوبة
        return request.user.is_authenticated and request.user.role in ["Admin", "HRM"]

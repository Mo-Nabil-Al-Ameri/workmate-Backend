from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobsAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'default_salary', 'short_description')  # عرض الحقول في القائمة
    search_fields = ('title', 'description')  # تمكين البحث في العنوان والوصف
    list_filter = ('default_salary',)  # تمكين الفلترة حسب الراتب الافتراضي
    ordering = ('title',)  # ترتيب السجلات حسب العنوان

    def short_description(self, obj):
        """إظهار جزء من الوصف في القائمة."""
        return obj.description[:50] + '...' if obj.description else 'No Description'
    short_description.short_description = 'Description'  # العنوان الظاهر في القائمة

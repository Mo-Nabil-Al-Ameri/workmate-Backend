from django.contrib import admin
from .models import User, Employee,Profile

# إدارة مخصصة لنموذج User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'role', 'is_active', 'last_login', 'gender')  # الأعمدة المعروضة
    list_filter = ('role', 'is_active', 'gender')  # عوامل التصفية
    search_fields = ('email', 'name', 'phone')  # الحقول التي يمكن البحث فيها
    ordering = ('-last_login',)  # ترتيب السجلات
    fieldsets = (  # حقول محرر التفاصيل
        (None, {'fields': ('email', 'name', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_active', 'role')}),
        ('Personal Info', {'fields': ('gender',)}),
    )
    add_fieldsets = (  # عند إضافة مستخدم جديد
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'phone', 'role', 'gender'),
        }),
    )
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# إدارة مخصصة لنموذج Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'department', 'job', 'salary', 'employee_number', 'employment_type')
    list_filter = ('department', 'employment_type', 'contract_type', 'marital_status')
    search_fields = ('email', 'name', 'phone', 'employee_number')
    ordering = ('-date_of_birth',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'phone', 'department', 'job', 'salary')}),
        ('Personal Info', {'fields': ('date_of_birth', 'marital_status', 'address', 'emergency_contact')}),
        ('Employment Info', {'fields': ('employment_type', 'contract_type', 'contract_end_date')}),
        ('Records', {'fields': ('disciplinary_record', 'training_record')}),
    )
    inlines = [ProfileInline]

from rest_framework import serializers
from .models import User, Employee,Profile
from .validators import validate_full_name, validate_email, validate_phone, validate_password, set_default_salary

from .utils import send_verification_email

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'password', 'role', 'gender']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # التحقق من الحقول
    def validate_name(self, value):
        validate_full_name(value)
        return value

    def validate_email(self, value):
        validate_email(value)
        return value

    def validate_phone(self, value):
        validate_phone(value)
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  
        user.save()
        send_verification_email(user)

        return user


class EmployeeSerializer(UserSerializer):
    class Meta:
        model = Employee
        fields = UserSerializer.Meta.fields + [
            'job', 'salary', 'department', 'date_of_birth', 'marital_status',
            'address', 'emergency_contact', 'employee_number', 'employment_type',
            'contract_type', 'contract_end_date', 'disciplinary_record', 'training_record'
        ]

    def create(self, validated_data):
        job = validated_data.get('job', None)
        if 'salary' not in validated_data or validated_data['salary'] is None:
            if job and hasattr(job, 'default_salary'):
                validated_data['salary'] = job.default_salary  # تعيين الراتب الافتراضي من الوظيفة
            else:
                validated_data['salary'] = 0  # تعيين قيمة افتراضية في حال عدم وجود وظيفة أو راتب افتراضي

        employee = Employee(**validated_data)
        employee.set_password(validated_data.pop('password'))  # تعيين كلمة المرور
        employee.save()
        send_verification_email(employee)

        return employee

# # Serializer للنموذج User
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             'id', 'email', 'name', 'phone', 'role', 'is_active', 
#             'last_login', 'gender'
#         ]  # الحقول التي يتم تضمينها في الـ API
#         read_only_fields = ['id', 'last_login']  # الحقول التي لا يمكن تعديلها


# # Serializer للنموذج Employee
# class EmployeeSerializer(serializers.ModelSerializer):
#     department_name = serializers.CharField(source='department.name', read_only=True)
#     job_title = serializers.CharField(source='job.title', read_only=True)

#     class Meta:
#         model = Employee
#         fields = [
#             'id', 'email', 'name', 'phone', 'department', 'department_name', 
#             'job', 'job_title', 'salary', 'date_of_birth', 'marital_status', 
#             'address', 'emergency_contact', 'employee_number', 'employment_type', 
#             'contract_type', 'contract_end_date', 'disciplinary_record', 'training_record'
#         ]
#         read_only_fields = ['id', 'employee_number']  # الحقول التي لا يمكن تعديلها

from rest_framework import serializers
from .models import User, Employee,Profile
from django.db import transaction
from .validators import (
    validate_full_name,
    validate_email,
    validate_phone,
    validate_password,
    set_default_salary,
)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer لتحديث بيانات الموظف العادي فقط (بما في ذلك الملف الشخصي)
    """
    profile = ProfileSerializer(required=False)  # تضمين بيانات الملف الشخصي

    class Meta:
        model = Employee
        fields = [
            "email", "name", "phone", "gender",
            "date_of_birth", "marital_status", "address", "emergency_contact",
            "profile"  # إضافة الملف الشخصي
        ]
        extra_kwargs = {
            "email": {"validators": [validate_email]},
            "name": {"validators": [validate_full_name]},
            "phone": {"validators": [validate_phone]},
        }

    def update(self, instance, validated_data):
        """
        تحديث بيانات الموظف مع دعم تحديث الملف الشخصي
        """
        profile_data = validated_data.pop("profile", None)  # استخراج بيانات الملف الشخصي
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # تحديث بيانات الموظف
        
        if profile_data:
            profile_instance = instance.profile  # جلب الملف الشخصي للموظف
            for attr, value in profile_data.items():
                setattr(profile_instance, attr, value)  # تحديث بيانات الملف الشخصي
            profile_instance.save()

        instance.save()
        return instance

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
        """إنشاء مستخدم جديد مع تشفير كلمة المرور"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)

        if password:
            user.set_password(password)  # تشفير كلمة المرور

        user.save()

        # ⚠️ بدلاً من إرسال البريد الإلكتروني هنا، يفضل استخدام signals.py
        # send_verification_email(user)

        return user

class EmployeeOutputSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(source='profile.photo')
    bio = serializers.CharField(max_length=255,source='profile.bio')
    class Meta:
        model = Employee
        fields = ['name', 'email', 'phone', 'role','photo', 'bio']

class EmployeeSerializer(UserSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'email', 'name', 'phone', 'password', 'role', 'gender', 
            'job', 'salary', 'department', 'date_of_birth', 'marital_status',
            'address', 'emergency_contact', 'employee_number', 'employment_type',
            'contract_type', 'contract_end_date', 'disciplinary_record', 'training_record'
        ]
        read_only_fields = ['employee_number']
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'email': {'validators': [validate_email]},
            'name': {'validators': [validate_full_name]},
            'phone': {'validators': [validate_phone]},
        }
        
        # extra_kwargs = {
        #     'password': {'write_only': True, 'help_text': 'Enter a strong password.'},
        #     'email': {'help_text': 'Enter the employee email address.'},
        #     'name': {'help_text': 'Enter the full name of the employee.'},
        #     'salary': {'help_text': 'Set the employee salary in decimal format.'},
        #     'job': {'help_text': 'Select the employee job (if applicable).'}
        # }

    def validate_salary(self, value):
        """التحقق من الراتب ليكون أكبر من الصفر"""
        if value is not None and value < 0:
            raise serializers.ValidationError("الراتب لا يمكن أن يكون سالبًا.")
        return value

    @transaction.atomic  # 🛑 اجعل العملية كاملة إما تتم أو يتم التراجع عنها
    def create(self, validated_data):
        password = validated_data.pop('password', None)  # إزالة كلمة المرور من البيانات
        job = validated_data.get('job', None)

        # """إنشاء مستخدم وموظف داخل معاملة ذرية"""
        # password = validated_data.pop('password', None)  # استخراج كلمة المرور
        # job = validated_data.get('job', None)

        try:
                
         # تعيين الراتب الافتراضي إذا لم يكن موجودًا
            if 'salary' not in validated_data or validated_data['salary'] is None:
                validated_data['salary'] = set_default_salary(job)

            # إنشاء الموظف
            user = Employee(**validated_data)
            if password:
                user.set_password(password)  # تشفير كلمة المرور
            user.save()
            return user
           # # **1️⃣ إنشاء مستخدم عادي (`User`)**
            # user_data = {key: validated_data[key] for key in ['email', 'name', 'phone', 'role', 'gender'] if key in validated_data}
            # user = User.objects.create(**user_data)

            # if password:
            #     user.set_password(password)  # تشفير كلمة المرور
            # user.save()

            # # **2️⃣ إعداد بيانات الموظف (`Employee`)**
            # employee_data = {key: validated_data[key] for key in [
            #     'job', 'salary', 'department', 'date_of_birth', 'marital_status',
            #     'address', 'emergency_contact', 'employment_type',
            #     'contract_type', 'contract_end_date', 'disciplinary_record', 'training_record'
            # ] if key in validated_data}

            # # **3️⃣ تعيين الراتب الافتراضي إذا لم يكن محددًا**
            # if 'salary' not in employee_data or employee_data['salary'] is None:
            #     employee_data['salary'] = set_default_salary(job)

            # # **4️⃣ إنشاء الموظف (`Employee`)**
            # employee = Employee.objects.create(user_ptr=user, **employee_data)

            # # **5️⃣ إرسال بريد التحقق بعد نجاح العملية**

            # return employee

        except Exception as e:
            # إذا حدث خطأ أثناء إنشاء الموظف، يتم التراجع عن كل شيء
            raise serializers.ValidationError(f"⚠ خطأ أثناء إنشاء الموظف: {str(e)}")


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100,style={'input_type':'password'},validators=[validate_password])
    new_password = serializers.CharField(max_length=100,style={'input_type':'password'},validators=[validate_password])
    confirm_password = serializers.CharField(max_length=100,style={'input_type':'password'},validators=[validate_password])

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"detail":"Passwords do not match"})
        return data
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'name', 'phone', 'password', 'role', 'gender']
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     # التحقق من الحقول
#     def validate_name(self, value):
#         validate_full_name(value)
#         return value

#     def validate_email(self, value):
#         validate_email(value)
#         return value

#     def validate_phone(self, value):
#         validate_phone(value)
#         return value

#     def validate_password(self, value):
#         validate_password(value)
#         return value

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)  
#         user.save()
#         send_verification_email(user)

#         return user

# class EmployeeSerializer(UserSerializer):
#     class Meta:
#         model = Employee
#         fields = UserSerializer.Meta.fields + [
#             'job', 'salary', 'department', 'date_of_birth', 'marital_status',
#             'address', 'emergency_contact', 'employee_number', 'employment_type',
#             'contract_type', 'contract_end_date', 'disciplinary_record', 'training_record'
#         ]

#     def create(self, validated_data):
#         job = validated_data.get('job', None)
#         if 'salary' not in validated_data or validated_data['salary'] is None:
#             if job and hasattr(job, 'default_salary'):
#                 validated_data['salary'] = job.default_salary  # تعيين الراتب الافتراضي من الوظيفة
#             else:
#                 validated_data['salary'] = 0  # تعيين قيمة افتراضية في حال عدم وجود وظيفة أو راتب افتراضي

#         employee = Employee(**validated_data)
#         employee.set_password(validated_data.pop('password'))  # تعيين كلمة المرور
#         employee.save()
#         send_verification_email(employee)

#         return employee

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

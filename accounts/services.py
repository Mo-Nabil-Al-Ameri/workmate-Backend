from .models import Employee
from rest_framework import serializers
from django.contrib.auth.models import Group

def user_update(
    user,
    name=None,
    email=None,
    phone=None,
    role=None,
    salary=None,
    department=None,
    job=None,
    address=None,
    emergency_contact=None,
    date_of_birth=None,
    marital_status=None
):
    """
    تحديث معلومات المستخدم (الموظف).
    """
    if name is not None:
        user.name = name
    if email is not None:
        if User.objects.exclude(id=user.id).filter(email=email).first():
            raise serializers.ValidationError({"detail":'Email already exists'})
        user.email = email
    if phone is not None:
        user.phone = phone
    if role is not None:
        user.role = role
        user.groups.clear()
        user.groups.add(Group.objects.get(name=role))
    if salary:
        user.salary = salary
    if department:
        user.department = department
    if job:
        user.job = job
    if address:
        user.address = address
    if emergency_contact:
        user.emergency_contact = emergency_contact
    if date_of_birth:
        user.date_of_birth = date_of_birth
    if marital_status:
        user.marital_status = marital_status
    user.profile.save()
    user.save()
    return user

from rest_framework import serializers
from django.contrib.auth import authenticate
from core.models import GlobalUser, Student, Professor


# ─────────────────────────────────────────────
# Auth Serializers
# ─────────────────────────────────────────────

class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(id=data.get('id'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("بيانات الدخول غير صحيحة.")
        if not user.is_active:
            raise serializers.ValidationError("هذا الحساب غير مفعل.")
        if user.is_locked:
            raise serializers.ValidationError("هذا الحساب مقفل (Locked).")
        return user


# ─────────────────────────────────────────────
# Profile Serializers
# ─────────────────────────────────────────────

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'university_id',
            'enrollment_year',
            'student_status',
            'department',
        ]


class ProfessorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = [
            'academic_rank',
            'department',
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField( read_only=True)
    department = serializers.StringRelatedField(read_only=True)
    student_profile = serializers.SerializerMethodField()
    professor_profile = serializers.SerializerMethodField()

    class Meta:
        model = GlobalUser
        fields = [
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'email_address',
            'role',
            'department',
            'is_active',
            'is_locked',
            'student_profile',
            'professor_profile',
        ]

    def get_student_profile(self, obj):
        if hasattr(obj, 'student'):
            return StudentProfileSerializer(obj.student).data
        return None

    def get_professor_profile(self, obj):
        if hasattr(obj, 'professor'):
            return ProfessorProfileSerializer(obj.professor).data
        return None
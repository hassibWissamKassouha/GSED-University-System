from rest_framework import serializers
from django.contrib.auth import authenticate
from core.models import GlobalUser

class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(id=data.get('id'), password=data.get('password'))
        if user and user.is_active:
            if user.isLocked:
                raise serializers.ValidationError("هذا الحساب مقفل (Locked).")
            return user
        raise serializers.ValidationError("بيانات الدخول غير صحيحة.")
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalUser
        fields = ['id', 'username', 'email', 'role', 'isLocked']
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import LoginSerializer, UserProfileSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'role': user.role.roleName if user.role else None,
                'name': f"{user.firstName} {user.lastName}"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    data = {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "permissions": list(user.get_all_permissions()), # قائمة بكل صلاحياته التقنية
    }

    # تخصيص البيانات الإضافية بناءً على الدور (أو الصلاحية)
    if user.role == 'Student':
        data['student_info'] = {
            "GPA": user.student_profile.gpa, # افتراض وجود علاقة OneToOne
            "year": user.student_profile.academic_year
        }
    elif user.role == 'Professor':
        data['professor_info'] = {
            "department": user.professor_profile.department,
            "office_hours": "10AM - 2PM"
        }
    elif user.role == 'Admin':
        data['admin_tools'] = ["user_management", "system_logs", "backups"]

    return Response(data)

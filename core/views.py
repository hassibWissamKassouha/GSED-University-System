from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import LoginSerializer, UserProfileSerializer
from .permissions import IsAdmin, IsProfessor, IsStudent, IsAdminOrStaff


# ─────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────

class LoginView(APIView):
    """
    POST /api/login/
    Authenticates a user and returns a token.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'role': user.role,
                'name': user.full_name,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    POST /api/logout/
    Deletes the user's token, effectively logging them out.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'تم تسجيل الخروج بنجاح.'}, status=status.HTTP_200_OK)


# ─────────────────────────────────────────────
# User Profile
# ─────────────────────────────────────────────

class UserProfileView(APIView):
    """
    GET /api/profile/
    Returns the authenticated user's profile.
    Automatically includes student or professor details based on their role.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
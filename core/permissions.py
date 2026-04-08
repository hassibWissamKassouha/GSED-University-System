from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Only Admin group members."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='Admin').exists()
        )


class IsProfessor(BasePermission):
    """Only Professor group members."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='Professor').exists()
        )


class IsStudent(BasePermission):
    """Only Student group members."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='Student').exists()
        )


class IsStaff(BasePermission):
    """Only Staff group members."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='Staff').exists()
        )


class IsProfessorOrAdmin(BasePermission):
    """Professor or Admin group members."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name__in=['Professor', 'Admin']).exists()
        )


class IsAdminOrStaff(BasePermission):
    """Admin or Staff group members."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name__in=['Admin', 'Staff']).exists()
        )


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission.
    Allows access if the user owns the object or is an Admin.
    The view must pass the object to check_object_permissions().
    The object must have a 'user' attribute pointing to a GlobalUser.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Admin').exists():
            return True
        # Support both direct user objects and related profile objects (student, professor)
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorOrStaffOrReadOnly(BasePermission):
    """Для регулирования контента, который создают пользователи."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous and request.method not in SAFE_METHODS:
            return False
        if (obj.author == request.user
           or request.user.is_moderator
           or request.user.is_admin):
            return True
        return False


class AdminOnly(BasePermission):
    """
    Для управления контентом, который создается администрацией и который
    не должен быть доступен для пользователей.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if (request.user.is_superuser
           or request.user.is_admin):
            return True
        return False


class AdminOrReadOnly:
    """
    Для управления контентом, который создается администрацией
    и который доступен для пользователй.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous and request.method not in SAFE_METHODS:
            return False
        if (request.user.is_superuser
           or request.user.is_admin):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if (request.user.is_superuser
           or request.user.is_admin):
            return True
        return False


class IsSelf(BasePermission):
    """Регулирует пользовательское управление своими персональными данными"""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user

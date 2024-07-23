from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Проверка, является ли пользователь модератором.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moder").exists()


class CanEditLessonOrCourse(BasePermission):
    """
    Разрешение на редактирование уроков и курсов для модераторов.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwner(BasePermission):
    """
    Проверка, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsNotModerator(BasePermission):
    """
    Проверка, что пользователь не является модератором.
    """

    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moder").exists()

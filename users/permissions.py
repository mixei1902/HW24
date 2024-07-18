from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Проверка, является ли пользователь модератором.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moder').exists()


class CanEditLessonOrCourse(BasePermission):
    """
    Разрешение на редактирование уроков и курсов для модераторов.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moder').exists() and request.method in ['PUT', 'PATCH', 'GET']

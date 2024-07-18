from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


from .models import Payment
from .serializers import UserSerializer, PaymentSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Представление для создания пользователя.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """
        Привязка пользователя и установка пароля.
        """
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListView(ListAPIView):
    """
    Представление для отображения списка пользователей.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления пользователя.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer


class LogoutView(APIView):
    """
    Представление для выхода из системы.
    """
    permission_classes = (IsAuthenticated,)



class PaymentListAPIView(ListAPIView):
    """
    Представление для отображения списка платежей.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']

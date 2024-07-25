from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .models import CoursePurchase
from .models import Payment, User
from .serializers import CoursePurchaseSerializer
from .serializers import UserSerializer, PaymentSerializer
from .services import create_stripe_price, create_stripe_session, convert_rub_to_dollars


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
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]


class CoursePurchaseCreateAPIView(CreateAPIView):
    serializer_class = CoursePurchaseSerializer
    queryset = CoursePurchase.objects.all()

    def perform_create(self, serializer):
        purchase = serializer.save(user=self.request.user)
        amount_in_dollars = convert_rub_to_dollars(purchase.amount)
        price = create_stripe_price(amount_in_dollars)
        session_id, payment_link = create_stripe_session(price.id)
        purchase.session_id = session_id
        purchase.link = payment_link
        purchase.save()

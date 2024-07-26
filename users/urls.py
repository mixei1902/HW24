from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .apps import UsersConfig
from .views import (
    UserCreateAPIView,
    UserListView,
    UserDetailView,
    LogoutView,
    PaymentListAPIView, CoursePurchaseCreateAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    # path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path('create-payment/', CoursePurchaseCreateAPIView.as_view(), name='create_payment'),
]

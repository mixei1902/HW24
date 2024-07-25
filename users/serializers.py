from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from .models import CoursePurchase
from .models import Payment


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели User.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "city",
            "avatar",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Создание нового пользователя с хешированным паролем.
        """
        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            city=validated_data["city"],
            avatar=validated_data["avatar"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class PaymentSerializer(ModelSerializer):
    """
    Сериализатор для модели Payment.
    """

    class Meta:
        model = Payment
        fields = "__all__"


class CoursePurchaseSerializer(ModelSerializer):
    class Meta:
        model = CoursePurchase
        fields = ['course', 'amount']

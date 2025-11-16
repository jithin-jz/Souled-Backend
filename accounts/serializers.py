from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


# -------------------------------
# USER SERIALIZER
# -------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
        )


# -------------------------------
# REGISTER SERIALIZER (FIXED)
# -------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")

    def create(self, validated_data):
        password = validated_data.pop("password")

        # 🔥 FIX: Use UserManager.create_user()
        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


# -------------------------------
# LOGIN SERIALIZER
# -------------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                "Email and password are required."
            )

        # Authenticate using email + password
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("User account disabled.")

        attrs["user"] = user
        return attrs

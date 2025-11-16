from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

from .serializers import RegisterSerializer, UserSerializer, LoginSerializer

User = get_user_model()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            data = UserSerializer(user).data

            return Response(
                {"user": data, "tokens": tokens},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = get_tokens_for_user(user)
            data = UserSerializer(user).data

            return Response(
                {"user": data, "tokens": tokens},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("id_token")

        if not token:
            return Response({"detail": "Missing id_token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            info = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                GOOGLE_CLIENT_ID
            )

            email = info.get("email")

            if not email:
                return Response({"detail": "Google token missing email"}, status=400)

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": info.get("given_name", ""),
                    "last_name": info.get("family_name", "")
                }
            )

            tokens = get_tokens_for_user(user)
            data = UserSerializer(user).data

            return Response(
                {"user": data, "tokens": tokens, "created": created},
                status=200
            )

        except ValueError:
            return Response({"detail": "Invalid Google token"}, status=400)

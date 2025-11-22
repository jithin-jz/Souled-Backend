import os
from django.conf import settings
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .authentication import AUTH_COOKIE_KEY, REFRESH_COOKIE_KEY

User = get_user_model()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def set_jwt_cookies(response, refresh: RefreshToken):
    """Attach access & refresh JWT tokens as HttpOnly cookies."""
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    secure = getattr(settings, "SECURE_COOKIES", False)

    # Access token: expires 1 hour
    response.set_cookie(
        AUTH_COOKIE_KEY,
        access_token,
        max_age=3600,
        httponly=True,
        secure=secure,
        samesite="Lax",
        path="/",
    )

    # Refresh token: expires 7 days
    response.set_cookie(
        REFRESH_COOKIE_KEY,
        refresh_token,
        max_age=3600 * 24 * 7,
        httponly=True,
        secure=secure,
        samesite="Lax",
        path="/",
    )


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        response = Response(
            {"user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )
        set_jwt_cookies(response, refresh)
        return response


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        response = Response(
            {"user": UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )
        set_jwt_cookies(response, refresh)
        return response


class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("id_token")
        if not token:
            return Response(
                {"detail": "Missing id_token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            info = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                GOOGLE_CLIENT_ID,
            )

            email = info["email"]
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": info.get("given_name", ""),
                    "last_name": info.get("family_name", ""),
                },
            )

            refresh = RefreshToken.for_user(user)

            response = Response(
                {"user": UserSerializer(user).data, "created": created},
                status=status.HTTP_200_OK,
            )
            set_jwt_cookies(response, refresh)
            return response

        except Exception:
            return Response(
                {"detail": "Invalid Google token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(APIView):
    """
    User logout does not require auth.
    Deletes cookies regardless of access token state.
    Prevents CSRF issues by disabling protection for this view only.
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        response = Response({"message": "Logged out"}, status=200)
        response.delete_cookie(AUTH_COOKIE_KEY, path="/")
        response.delete_cookie(REFRESH_COOKIE_KEY, path="/")
        return response


class RefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_KEY)
        if not refresh_token:
            return Response({"detail": "No refresh cookie"}, status=401)

        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token

            response = Response({"detail": "Access refreshed"}, status=200)

            response.set_cookie(
                AUTH_COOKIE_KEY,
                str(new_access),
                max_age=3600,
                httponly=True,
                secure=getattr(settings, "SECURE_COOKIES", False),
                samesite="Lax",
                path="/",
            )
            return response

        except Exception:
            return Response({"detail": "Refresh invalid"}, status=401)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            UserSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )

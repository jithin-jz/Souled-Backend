from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions

# Will look in settings.SIMPLE_JWT["AUTH_COOKIE"], fallback to "access"
AUTH_COOKIE_KEY = getattr(settings, "SIMPLE_JWT", {}).get("AUTH_COOKIE", "access")
REFRESH_COOKIE_KEY = getattr(settings, "SIMPLE_JWT", {}).get("AUTH_COOKIE_REFRESH", "refresh")

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
CSRF_PROTECTED_METHODS = ("POST", "PUT", "PATCH", "DELETE")


def enforce_csrf(request):
    """
    Proper CSRF validation using DRF's CSRFCheck wrapper.
    """
    check = CSRFCheck(lambda r: None)
    check.process_request(request)
    reason = check.process_view(request, None, (), {})

    if reason:
        raise exceptions.PermissionDenied(f"CSRF Failed: {reason}")


class CookieJWTAuthentication(JWTAuthentication):
    """
    Authentication class that reads the JWT access token from an HTTP only cookie.
    Works with SimpleJWT.
    
    CSRF checking is handled at the view level using @csrf_exempt decorators.
    """
    def authenticate(self, request):
        token = request.COOKIES.get(AUTH_COOKIE_KEY)
        if token is None:
            return None

        # CSRF is now handled by @csrf_exempt decorators on views
        # This allows granular control over which endpoints need CSRF protection

        try:
            validated_token = self.get_validated_token(token)
        except Exception:
            # Invalid or expired token
            return None

        user = self.get_user(validated_token)
        
        # Check if user is blocked
        if user and user.is_block:
            raise exceptions.AuthenticationFailed("Your account has been blocked. Please contact support.")
        
        return user, validated_token

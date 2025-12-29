from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    GoogleLoginView,
    LogoutView,
    MeView,
    RefreshView,
    ProfileUpdateView,
    NotificationListAPIView,
    MarkNotificationReadAPIView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
    path("google/", GoogleLoginView.as_view(), name="google_login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("update-profile/", ProfileUpdateView.as_view(), name="update_profile"),
    path("notifications/", NotificationListAPIView.as_view(), name="notification_list"),
    path("notifications/<int:pk>/read/", MarkNotificationReadAPIView.as_view(), name="notification_read"),
]

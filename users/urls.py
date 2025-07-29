# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("auth/signup/", views.SignUpView.as_view(), name="auth-signup"),
    path("auth/login/", views.TokenObtainPairView.as_view(), name="auth-login"),
    path("users/me/", views.UserMeView.as_view(), name="user-me"),
    path("users/<int:user_id>/", views.UserDetailView.as_view(), name="user-detail"),
]

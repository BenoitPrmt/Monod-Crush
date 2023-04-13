from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from .views import RegisterView

# app_name = 'authentication'

urlpatterns = [
    path("login", LoginView.as_view(template_name="authentication/login.html"), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("logout", LogoutView.as_view(next_page="/"), name="logout"),
    path("password-change", PasswordChangeView.as_view(), name="password_change"),
    path("password-change/done", PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password-reset", PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

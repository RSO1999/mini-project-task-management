from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True, next_page="profile"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("change-password/", auth_views.PasswordChangeView.as_view(), name="change_password"),
    path("profile/", views.profile, name="profile"),
    ] 

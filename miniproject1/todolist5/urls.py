
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('todo-page', views.todo_page, name='todo_page'),
    path("todo/<int:pk>/edit/", views.TodoItemUpdateView.as_view(),
         name="edit_todo"),  # Edit page
    path("register/", views.register, name="register"),
    path("login/", views.todo_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("change-password/", views.edit_password, name="change_password"),
    path("profile/", views.profile, name="profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
]

from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from . import views
from .views import AddTodoItemView, home, BulkDeleteTodoView

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True, next_page="profile"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("change-password/", auth_views.PasswordChangeView.as_view(), name="change_password"),
    path("profile/", views.profile, name="profile"),
    path('todo-page', views.todo_page, name='todo_page'),
    path('add/', AddTodoItemView.as_view(), name='add_todo_item'),
    path('delete-items/', views.delete_todo_item, name='delete_todo_item'),
    path('confirm-bulk-delete/',views.BulkDeleteTodoView.as_view(), name='confirm_bulk_delete'),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    ] 

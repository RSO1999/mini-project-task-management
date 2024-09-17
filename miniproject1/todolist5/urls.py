
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import AddTodoItemView, home, BulkDeleteTodoView



urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.todo_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path('todo-page', views.todo_page, name='todo_page'),
    path("change-password/", views.edit_password, name="change_password"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path('add/', AddTodoItemView.as_view(), name='add_todo_item'),
    path('delete-items/', views.delete_todo_item, name='delete_todo_item'),
    path("todo/<int:pk>/edit/", views.TodoItemUpdateView.as_view(), name="edit_todo"),  # Edit page
    path('confirm-bulk-delete/',views.BulkDeleteTodoView.as_view(), name='confirm_bulk_delete'),
    ] 
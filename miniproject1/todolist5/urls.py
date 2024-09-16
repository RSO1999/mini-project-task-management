from django.urls import path
from . import views
from .views import AddTodoItemView, home, BulkDeleteTodoView

urlpatterns = [
    path("", views.home, name="home"),
    path('todo-page', views.todo_page, name='todo_page'),
    path('add/', AddTodoItemView.as_view(), name='add_todo_item'),
    path('delete-items/', views.delete_todo_item, name='delete_todo_item'),
    path('confirm-bulk-delete/',views.BulkDeleteTodoView.as_view(), name='confirm_bulk_delete'),
]
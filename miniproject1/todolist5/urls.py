
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


# http://localhost:8000/
urlpatterns = [
     
     #AUTH/ACCOUNTS
     path("", views.todo_login, name="login"),
     path("register/", views.register, name="register"),
     path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
     path("change-password/", views.edit_password, name="change_password"),
     path("edit-profile/", views.edit_profile, name="edit_profile"),
     
     #PERSONAL TODOLIST
     path('todos/<int:user_id>/todolist/', views.personal_todo_page, name='personal_todo_page'),
     path('todos/<int:user_id>/add-todo/', views.add_personal_todo_item, name='add_personal_todo_item'),
     path('todos/<int:user_id>/edit-todo/<int:todo_id>/', views.edit_personal_todo_item, name="edit_personal_todo_item"),
     path('todos/<int:user_id>/delete-todo/', views.delete_personal_todo_item, name='delete_personal_todo_item'),
     path('todos/<int:user_id>/confirm-todo-deletion/', views.confirm_personal_bulk_delete, name='confirm_personal_bulk_delete'),
     
     #TEAMS
     path('team/create_team/', views.create_team, name='create_team'),
     path('team/<int:team_id>/edit_team/', views.edit_team, name='edit_team'),
     
     #TEAM TODOLIST
     path('team/<int:team_id>/todolist/', views.team_todo_page, name='team_todo_page'),
     # path('team/<int:team_id>/add-todo/', views.add_team_todo_item, name='add_team_todo_item'),
     # path("team/<int:team_id>/edit-todo/<int:todo_id>/", views.edit_team_todo_item, name="edit_team_todo_item"),
     # path('team/<int:team_id>/delete-todo/', views.delete_team_todo_item, name='delete_team_todo_item'),
     # path('team/<int:team_id>/confirm-todo-deletion/', views.confirm_team_bulk_delete, name='confirm_team_bulk_delete')
]

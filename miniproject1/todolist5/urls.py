
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("todo/<int:pk>/edit/", views.TodoItemUpdateView.as_view(),
         name="edit_todo"),  # Edit page
]

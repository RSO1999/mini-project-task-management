
from django.contrib import admin
from .models import TodoUser, TodoItem

# 1
admin.site.register(TodoItem)
admin.site.register(TodoUser)

from django.contrib import admin
from .models import TodoUser, TodoItem

# Register your models here.

admin.site.register(TodoItem)
admin.site.register(TodoUser) 

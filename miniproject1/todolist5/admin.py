
from django.contrib import admin
from .models import TodoUser, TodoItem

# Register your models here.
'''
@admin.register(TodoUser)
class TodoUserAdmin(admin.ModelAdmin):
    pass
'''
admin.site.register(TodoItem)
admin.site.register(TodoUser) 
'''
@admin.register(TodoUser)
class TodoUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')  # Example fields to display

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')  # Example fields to display
'''

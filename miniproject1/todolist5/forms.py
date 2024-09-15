from django import forms
from .models import TodoItem


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'description','due_date', 'priority']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'priority': forms.Select(choices=TodoItem.LEVEL_CHOICES),
        }
        
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
        
from django.contrib.auth.forms import  UserCreationForm
from django import forms
from . import models
class AccountRegistration(UserCreationForm):
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Username')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput) 
   
    class Meta:
        model = models.User
        fields = ['email', 'username', 'password1', 'password2']

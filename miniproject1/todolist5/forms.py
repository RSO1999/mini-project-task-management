from .models import TodoUser, TodoItem
from django import forms
from .models import TodoItem
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms
from .models import TodoUser

# class AccountRegistration(UserCreationForm):
# email = forms.EmailField(label='Email')
# username = forms.CharField(label='Username')
# password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
# assword2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

# class Meta:
# model = models.User
# fields = ['email', 'username', 'password1', 'password2']


class AccountRegistration(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(AccountRegistration, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required': 'True',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Username',
            'minlength': '5',
            'maxlength': '20',
        })
        self.fields['email'].widget.attrs.update({
            'required': 'True',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'class': 'form-control',
            'placeholder': 'name@example.com',
        })
        self.fields['password1'].widget.attrs.update({
            'required': 'True',
            'name': 'password1',
            'id': 'password1',
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Password',
            'minlength': '8',
        })
        self.fields['password2'].widget.attrs.update({
            'required': 'True',
            'name': 'password2',
            'id': 'password2',
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'minlength': '8',
        })

    class Meta:
        model = TodoUser
        fields = ['email', 'username', 'password1', 'password2']


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required': 'True',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Username',
            'minlength': '5',
            'maxlength': '20',
        })
        self.fields['email'].widget.attrs.update({
            'required': 'True',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'class': 'form-control',
            'placeholder': ''
        })

    class Meta:
        model = TodoUser
        fields = ['username', 'email']

    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)


class EditPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(EditPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'required': 'True',
            'name': 'password1',
            'id': 'password1',
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Password',
            'minlength': '8',
        }),
        self.fields['new_password2'].widget.attrs.update({
            'required': 'True',
            'name': 'password2',
            'id': 'password2',
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'minlength': '8',
        })

    class Meta:
        model = TodoUser
        fields = ['new_password1', 'new_password2']


class TodoItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(TodoItemForm, self).__init__(*args, **kwargs)
        

        # adds calendar feature
        self.fields['due_date'].widget = forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'placeholder': 'Select Due Date'
        })
        
        self.fields['reminder_date'].widget = forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'placeholder': 'Select Due Date',
        })

    class Meta:
        model = TodoItem
        fields = ['user', 'team', 'title', 'description', 'completed',
                  'due_date', 'priority', 'category', 'assignee', 'reminder_date']
        widgets = {
            'priority': forms.Select(choices=TodoItem.LEVEL_CHOICES),
        }


class AccountRegistration(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(AccountRegistration, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required': 'True',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Username',
            'minlength': '5',
            'maxlength': '20',
        })
        self.fields['email'].widget.attrs.update({
            'required': 'True',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'class': 'form-control',
            'placeholder': 'name@example.com',
        })
        self.fields['password1'].widget.attrs.update({
            'required': 'True',
            'name': 'password1',
            'id': 'password1',
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Password',
            'minlength': '8',
        })
        self.fields['password2'].widget.attrs.update({
            'required': 'True',
            'name': 'password2',
            'id': 'password2',
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'minlength': '8',
        })

    class Meta:
        model = TodoUser
        fields = ['email', 'username', 'password1', 'password2']


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required': 'True',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Username',
            'minlength': '5',
            'maxlength': '20',
        })
        self.fields['email'].widget.attrs.update({
            'required': 'True',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'class': 'form-control',
            'placeholder': ''
        })

    class Meta:
        model = TodoUser
        fields = ['username', 'email']

    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)


class EditPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(EditPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'required': 'True',
            'name': 'password1',
            'id': 'password1',
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Password',
            'minlength': '8',
        }),
        self.fields['new_password2'].widget.attrs.update({
            'required': 'True',
            'name': 'password2',
            'id': 'password2',
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'minlength': '8',
        })

    class Meta:
        model = TodoUser
        fields = ['new_password1', 'new_password2']

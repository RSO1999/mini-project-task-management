from .models import TodoUser, TodoItem
from django import forms
from .models import TodoItem
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms
from .models import TodoUser, TodoTeam
from django.core.mail import send_mail
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
            'placeholder': 'Select Reminder Date'
        })

    class Meta:
        model = TodoItem
        fields = ['user', 'team', 'title', 'description', 'completed',
                  'due_date', 'priority', 'category', 'assignee', 'reminder_date']
        widgets = {
            'priority': forms.Select(choices=TodoItem.LEVEL_CHOICES),
        }

class TodoTeamForm(forms.ModelForm):
    class Meta:
        model = TodoTeam
        fields = ['name', 'description', 'users']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter team name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter team description', 'class': 'form-control', 'rows': 3}),
            'users': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if self.current_user:
            self.fields['users'].queryset = TodoUser.objects.exclude(id=self.current_user.id)

    def clean_users(self):
        users = self.cleaned_data.get('users', [])
        if not users:
            raise forms.ValidationError("You must select at least one user.")
        return users

    def save(self, commit=True):
        team = super().save(commit=False)
        if commit:
            team.save()  
            team.users.add(self.current_user)  
            
            for user in self.cleaned_data.get('users', []):
                if user not in team.users.all():  
                    team.users.add(user)

            for user in self.cleaned_data['users']:
                send_mail(
                    'You have been invited to join a team on the Group 5 Todo App',
                    f'You have been invited to join the team: {team.name}.',
                    "csc394.group5@gmail.com",
                    [user.email],
                )
        return team
    
class EditTodoTeamForm(forms.ModelForm):
    class Meta:
        model = TodoTeam
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter updated team name', 'class': 'form-control', 'default': {TodoTeam.name}}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter updated team description', 'class': 'form-control', 'rows': 3, 'default': {TodoTeam.description}}),
        }




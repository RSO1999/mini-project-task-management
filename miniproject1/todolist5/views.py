from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.views import View
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.db import models
from django.db.models import Case, When, IntegerField
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.views.generic.edit import FormView
from django.contrib import messages
from .models import TodoItem, TodoUser, TodoTeam
from .forms import EditTodoTeamForm, TodoItemForm, AccountRegistration, EditProfileForm, EditPasswordForm, TodoTeamForm

#-----------------
#PERSONAL TODOLIST
#-----------------

def personal_todo_page(request, user_id):
    todos = TodoItem.objects.filter(user_id=user_id)
    
    search_query = request.GET.get("todo_search", "")
    
    sort_by = request.GET.get('sort', 'due_date')
    
    todos = todos.filter(
        models.Q(title__icontains=search_query) |
        models.Q(description__icontains=search_query)
    )
    
    if sort_by == 'priority':
        todos = todos.order_by(
            Case(
                When(priority='H', then=1),
                When(priority='M', then=2),
                When(priority='L', then=3),
                output_field=IntegerField()
            )
        )
    else:
        todos = todos.order_by('due_date')
    context = {
        'user_id': user_id,
        'todos': todos,
        'sort_by': sort_by,
        'search_query': search_query
    }
    return render(request, "todo_page.html", context)

def add_personal_todo_item(request, user_id):
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.user = request.user 
            todo_item.save()
            messages.success(request, "To-do item added successfully!")
            return redirect(reverse('personal_todo_page', kwargs={'user_id': request.user.id}))
    else:
        form = TodoItemForm() 

    return render(request, 'add_todo_item.html', {'form': form, 'user_id': user_id})

def edit_personal_todo_item(request, user_id, todo_id):
    todo_item = get_object_or_404(TodoItem, id=todo_id, user=request.user)  # Fetch the todo item

    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo_item)  # Bind the form to the existing instance
        if form.is_valid():
            form.save()  # Save the updated todo item
            messages.success(request, "To-do item updated successfully!")
            return redirect(reverse('personal_todo_page', kwargs={'user_id': user_id}))  # Redirect to the todo page
    else:
        form = TodoItemForm(instance=todo_item)  # Create a form instance for GET requests

    return render(request, 'edit_todo.html', {'form': form, 'user_id': user_id, 'todo_item': todo_item})

def delete_personal_todo_item(request, user_id):
    todo_items = TodoItem.objects.filter(user_id=user_id)
    return render(request, 'deleteTodo.html', {'user_id': user_id, 'todo_items': todo_items})

def confirm_personal_bulk_delete(request, user_id):
    if request.method == 'POST':
        selected_items = request.POST.getlist('todo_ids')
        if selected_items:
            TodoItem.objects.filter(id__in=selected_items).delete()

        return redirect(reverse('personal_todo_page', kwargs={'user_id': request.user.id}))  # Redirect to the todo page

    # If not a POST request, you might want to handle it accordingly (e.g., show an error or redirect)
    return redirect(reverse('personal_todo_page', kwargs={'user_id': request.user.id}))  # Redirect for non-POST requests
    
    
    
#-----------------
#TEAM TODOLIST
#-----------------

def team_todo_page(request, team_id):
    team = TodoTeam.objects.get(id=team_id)
    print(f"Users in team: {team.users.all()}")
    return render(request, "team_todo_page.html", {"team_id":team_id, "team": team})
    
    
#-----------------
#TEAM LOGIC
#-----------------
    
def create_team(request):
    if request.method == "POST":
        form = TodoTeamForm(request.POST, current_user=request.user)
        if form.is_valid():
            team = form.save() 
            messages.success(request, "Team created successfully.")
            return redirect(reverse('team_todo_page', kwargs={'team_id': team.id})) 
        else:
            messages.error(request, "There was an error creating the team. Please check the form.")
    else:
        form = TodoTeamForm(current_user=request.user)

    return render(request, "create_team.html", {"form": form})

def edit_team(request, team_id):
    team = TodoTeam.objects.get(id=team_id)
    if request.method == "POST":
        form = EditTodoTeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, "Team updated successfully.")
            return redirect(reverse('team_todo_page', kwargs={'team_id': team.id}))
    else:
        form = EditTodoTeamForm(instance=team)
    return render(request, "edit_team.html", {"form": form, "team": team})

def delete_team(request, team_id):
    team = TodoTeam.objects.get(id=team_id)
    if request.method == "POST":
        team = get_object_or_404(TodoTeam, id=team_id)
        team.delete()
        messages.success(request, f"Team {team.name} deleted successfully.")
        return redirect("personal_todo_page", user_id=request.user.id)
    return render(request, "delete_team.html", {"team": team})

#AUTH

def todo_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("personal_todo_page", user_id= user.id)
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        form = AccountRegistration(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            form.save()
            send_mail(
                'Welcome to the Group 5 Todo App',
                'Thank you for registering with us!',
                "{csc394.group5@gmail.com}",
                [email],
                fail_silently=False,
            )
            messages.success(
                request, "Registration successful! Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Invalid registration details.")
            return render(request, "register.html", {"error": "Invalid registration details.", "form": form})
    form = AccountRegistration()
    return render(request, "register.html", {"form": form})

def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
    return render(request, "edit_profile.html", {"form": EditProfileForm(instance=request.user)})


def edit_password(request):
    if request.method == "POST":
        form = EditPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Password updated successfully. Please log in again.")
            return redirect("login")
    return render(request, "edit_password.html", {"form": EditPasswordForm(user=request.user)})
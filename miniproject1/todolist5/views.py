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
from .models import TodoItem, TeamInvite, TodoTeam
from .forms import EditTodoTeamForm, TodoItemForm, AccountRegistration, EditProfileForm, EditPasswordForm, TodoTeamForm
from django.contrib.auth.decorators import login_required

#-----------------
#PERSONAL TODOLIST
#-----------------

def personal_todo_page(request, user_id):
    todos = TodoItem.objects.filter(user_id=user_id)
    
    search_query = request.GET.get("todo_search", "")
    
    sort_by = request.GET.get('sort', 'due_date')
    selected_category = request.GET.get('category', 'All')
    show_archive = request.GET.get('archive', 'false')

    # search filter
    if search_query:
        todos = todos.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    # category filter
    if selected_category != 'All':
        todos = todos.filter(category=selected_category)

    # Apply sorting
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

    # filters for completed tasks when button is clicked
    if show_archive == 'true':
        todos = todos.filter(completed__gte=100.00)

    # Filters by category
    categories = TodoItem.objects.filter(
        user=request.user).values_list('category', flat=True).distinct()

    # Pass the sorted or filtered list of todoItems to the template
    context = {
        'user_id': user_id,
        'todos': todos,
        'sort_by': sort_by,
        'search_query': search_query,
        'categories': categories,
        'selected_category': selected_category,
        'show_archive': show_archive,
    }
    return render(request, "personal/todo_page.html", context)

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

    return render(request, 'personal/add_todo.html', {'form': form, 'user_id': user_id})

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

    return render(request, 'personal/edit_todo.html', {'form': form, 'user_id': user_id, 'todo_item': todo_item})

def delete_personal_todo_item(request, user_id):
    todo_items = TodoItem.objects.filter(user_id=user_id)
    return render(request, 'personal/delete_todo.html', {'user_id': user_id, 'todo_items': todo_items})

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
    return render(request, "teams/team_todo_page.html", {"team_id":team_id, "team": team})
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

    return render(request, "teams/create_team.html", {"form": form})

def team_invite_confirmation(request, team_id, user_id):
    if not request.user.is_authenticated:
         return redirect(f"{reverse('login')}?next={request.path}")

    invite = get_object_or_404(TeamInvite, team_id=team_id, invited_user_id=user_id)

    if invite.is_accepted:
        messages.error(request, "You have already accepted the invitation.")
    else:
        invite.is_accepted = True
        invite.save()
        team = invite.team
        team.users.add(invite.invited_user)
        messages.success(request, f"Invitation accepted. You are now a member of team {team.name}.")
        return redirect(reverse('team_todo_page', kwargs={'team_id': team_id}))
    
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
    return render(request, "teams/edit_team.html", {"form": form, "team": team})

def delete_team(request, team_id):
    team = TodoTeam.objects.get(id=team_id)
    if request.method == "POST":
        team = get_object_or_404(TodoTeam, id=team_id)
        team.delete()
        messages.success(request, f"Team {team.name} deleted successfully.")
        return redirect("personal_todo_page", user_id=request.user.id)
    return render(request, "teams/delete_team.html", {"team": team})

#AUTH

def todo_login(request):
    next_page = request.GET.get('next', '') 
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            
            next_post = request.POST.get('next', '')
            if next_post:
                return redirect(next_post)
            return redirect("personal_todo_page", user_id=user.id)
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, "auth/login.html", {'next': next_page})



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
            return render(request, "auth/register.html", {"error": "Invalid registration details.", "form": form})
    form = AccountRegistration()
    return render(request, "auth/register.html", {"form": form})


def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
    return render(request, "auth/edit_profile.html", {"form": EditProfileForm(instance=request.user)})


def edit_password(request):
    if request.method == "POST":
        form = EditPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Password updated successfully. Please log in again.")
            return redirect("login")
    return render(request, "auth/edit_password.html", {"form": EditPasswordForm(user=request.user)})
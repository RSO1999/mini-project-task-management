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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


#-----------------
#PERSONAL TODOLIST
#-----------------

def personal_todo_page(request, user_id):

    # If the user selects team from the dropdown, redirect to the team's todo page
    team_id = request.GET.get('team_id', None)
    if team_id:
        return redirect("team_todo_page", team_id=team_id)
    
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
    
   
    user_teams = TodoTeam.objects.filter(users = request.user)

    
    context = {
        'user_id': user_id,
        'todos': todos,
        'sort_by': sort_by,
        'search_query': search_query,
        'categories': categories,
        'selected_category': selected_category,
        'show_archive': show_archive,
        'teams': user_teams,
    }
    return render(request, "personal/todo_page.html", context)

def add_personal_todo_item(request, user_id):
    if request.method == 'POST':
        form = TodoItemForm(request.POST, user=request.user)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.user = request.user 
            todo_item.save()
            messages.success(request, "To-do item added successfully!")
            return redirect(reverse('personal_todo_page', kwargs={'user_id': request.user.id}))
    else:
        form = TodoItemForm(user=request.user) 

    return render(request, 'personal/add_todo.html', {'form': form, 'user_id': user_id})

def edit_personal_todo_item(request, user_id, todo_id):
    todo_item = get_object_or_404(TodoItem, id=todo_id, user=request.user)

    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo_item, user=request.user)  
        if form.is_valid():
            form.save()  
            messages.success(request, "To-do item updated successfully!")
            return redirect(reverse('personal_todo_page', kwargs={'user_id': user_id}))
    else:
        form = TodoItemForm(instance=todo_item, user=request.user)

    return render(request, 'personal/edit_todo.html', {'form': form, 'user_id': user_id, 'todo_item': todo_item})

def delete_personal_todo_item(request, user_id):
    todo_items = TodoItem.objects.filter(user_id=user_id)
    return render(request, 'personal/delete_todo.html', {'user_id': user_id, 'todo_items': todo_items})

def confirm_personal_bulk_delete(request, user_id):
    if request.method == 'POST':
        selected_items = request.POST.getlist('todo_ids')
        if selected_items:
            TodoItem.objects.filter(id__in=selected_items).delete()

        return redirect(reverse('personal_todo_page', kwargs={'user_id': request.user.id})) 

    return redirect(reverse('personal_todo_page', kwargs={'user_id': request.user.id}))
    
    
    
#-----------------
#TEAM TODOLIST
#-----------------

def team_todo_page(request, team_id):
    team = TodoTeam.objects.get(id=team_id)
    print(f"Users in team: {team.users.all()}")

    todos = TodoItem.objects.filter(team_id=team_id)
    
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
        team_id=team_id).values_list('category', flat=True).distinct()

    context = {
        'team': team,
        'team_id': team_id,
        'todos': todos,
        'sort_by': sort_by,
        'search_query': search_query,
        'categories': categories,
        'selected_category': selected_category,
        'show_archive': show_archive,
    }
    return render(request, "teams/team_todo_page.html", context)

def add_team_todo_item(request, team_id):
    team = TodoTeam.objects.get(id=team_id)
    if request.method == 'POST':
        form = TodoItemForm(request.POST, team=team)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.team = team
            todo_item.save()
            messages.success(request, "To-do item added successfully!")
            return redirect(reverse('team_todo_page', kwargs={'team_id': team.id}))
    else:
        form = TodoItemForm(team=team) 

    return render(request, 'teams/team_add_todo.html', {'form': form, 'team_id': team_id, 'team': team})

def edit_team_todo_item(request, team_id, todo_id):
    team = TodoTeam.objects.get(id=team_id)
    todo_item = get_object_or_404(TodoItem, id=todo_id, team=team)

    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo_item, team=team)
        if form.is_valid():
            form.save()
            messages.success(request, "To-do item updated successfully!")
            return redirect(reverse('team_todo_page', kwargs={'team_id': team_id}))
    else:
        form = TodoItemForm(instance=todo_item, team=team) 
    return render(request, 'teams/team_edit_todo.html', {'form': form, 'team_id': team_id, 'team': team, 'todo_item': todo_item})

def delete_team_todo_item(request, team_id):
    team = TodoTeam.objects.get(id=team_id)
    todo_items = TodoItem.objects.filter(team_id=team_id)
    return render(request, 'teams/team_delete_todo.html', {'team_id': team_id, 'team': team, 'todo_items': todo_items})

def confirm_team_bulk_delete(request, team_id):
    team = TodoTeam.objects.get(id=team_id)
    if request.method == 'POST':
        selected_items = request.POST.getlist('todo_ids')
        if selected_items:
            TodoItem.objects.filter(id__in=selected_items).delete()

        return redirect(reverse('team_todo_page', kwargs={'team_id': team_id}))

    return redirect(reverse('team_todo_page', kwargs={'team_id': team.id}))



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



def delete_team_todo_list(request, team_id):
    team = TodoTeam.objects.get(id=team_id)
    todo_items = TodoItem.objects.filter(team_id=team_id)
    return render(request, 'teams/team_todo_page.html', {'team_id': team_id, 'team': team, 'todo_items': todo_items})


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
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import TodoItem 
from django.http import HttpResponseRedirect
from .forms import TodoItemForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView
from django.views import View
from django.core.mail import send_mail
from .forms import AccountRegistration
from django.shortcuts import redirect, render, HttpResponse
from django.core.mail import send_mail
from .forms import AccountRegistration, EditProfileForm, EditPasswordForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
from .models import TodoUser
# Create your views here.
  


    
def home(request):
    return render(request, "home.html")



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
            messages.success(request, "Registration successful! Please log in.")
            return redirect("/login/")
        else:
            messages.error(request, "Invalid registration details.")
            return render(request, "register.html", {"error": "Invalid registration details.", "form": form})
    form = AccountRegistration()
    return render(request, "register.html", {"form": form})

def todo_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(user)
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, "login.html")

def profile(request):
    return render(request, "profile.html")

def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    return render(request, "edit_profile.html", {"form": EditProfileForm(instance=request.user)})

def edit_password(request):
    if request.method == "POST":
        form = EditPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password updated successfully. Please log in again.")
            return redirect("login")
    return render(request, "edit_password.html", {"form": EditPasswordForm(user=request.user)})

def todo_page(request):
    todos = TodoItem.objects.all()
    return render(request, 'todo_page.html', {'todos':todos})
    
class AddTodoItemView(FormView):
    template_name = 'add_todo_item.html'
    form_class = TodoItemForm 
    success_url = reverse_lazy('todo_page')

    def form_valid(self, form):
        todo_item = form.save(commit=False)  
        if self.request.user.is_authenticated:
            todo_item.user = self.request.user  
        todo_item.save()  
        return super().form_valid(form)

def delete_todo_item(request):
    todo_items = TodoItem.objects.all()
    return render(request, 'deleteTodo.html', {'todo_items': todo_items})

class BulkDeleteTodoView(View):
    success_url = reverse_lazy('delete_todo_item')

    def post(self,request, *args, **kwargs):
        selected_items = request.POST.getlist('todo_ids')
        if selected_items:
            TodoItem.objects.filter(id__in=selected_items).delete()

        return redirect(self.success_url)
        
        return render(request, self.template_name, {'todo_ids': selected_items})

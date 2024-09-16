from django.shortcuts import redirect, render, HttpResponse
from django.core.mail import send_mail
from .forms import AccountRegistration, EditProfileForm, EditPasswordForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

    
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
        user = authenticate(request, email=email, password=password)
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



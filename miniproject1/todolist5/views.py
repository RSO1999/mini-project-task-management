from django.shortcuts import redirect, render, HttpResponse
from django.core.mail import send_mail
from .forms import AccountRegistration
# Create your views here.

    
def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        form = AccountRegistration(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            form.save()
            # send_mail(
            #     'Welcome to the Group 5 Todo App',
            #     'Thank you for registering with us!',
            #     "{insert your email here}",
            #     [email],
            #     fail_silently=False,
            # )
            return redirect("/login/")
    form = AccountRegistration()
    return render(request, "register.html", {"form": form})

def profile(request):
    return render(request, "profile.html")


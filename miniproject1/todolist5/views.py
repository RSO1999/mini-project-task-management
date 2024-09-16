from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import TodoItem 
from django.http import HttpResponseRedirect
from .forms import TodoItemForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView
from django.views import View
from django.core.mail import send_mail
from .forms import AccountRegistration
# Create your views here.

    
def home(request):
    todos = TodoItem.objects.all()
    return render(request, "home.html", {'todos': todos})

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
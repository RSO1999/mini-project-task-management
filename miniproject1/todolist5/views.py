
from django.shortcuts import render, HttpResponse
from .models import TodoItem
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import TodoItem
from .forms import TodoItemForm


class TodoItemUpdateView(UpdateView):
    model = TodoItem
    form_class = TodoItemForm
    # this is needed in order to see the Edit Page
    template_name = 'edit_todo.html'
    # Redirects back to the home page after edit
    success_url = reverse_lazy('home')


def home(request):
    # shows list
    todos = TodoItem.objects.all()
    return render(request, "home.html", {'todos': todos})

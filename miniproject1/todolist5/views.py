
from django.shortcuts import render, HttpResponse
from .models import TodoItem
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import TodoItem
from .forms import TodoItemForm
from django.db.models import Case, When, IntegerField


class TodoItemUpdateView(UpdateView):
    model = TodoItem
    form_class = TodoItemForm
    # this is needed in order to see the Edit Page
    template_name = 'edit_todo.html'
    # Redirects back to the home page after edit
    success_url = reverse_lazy('home')


def home(request):
    sort_by = request.GET.get('sort', 'due_date')
    if sort_by == 'priority':
        # Sort
        todos = TodoItem.objects.all().order_by(

            Case(

                When(priority='H', then=1),
                When(priority='M', then=2),
                When(priority='L', then=3),
                output_field=IntegerField()
            )
        )
    else:
        # due date sorting

        todos = TodoItem.objects.all().order_by('due_date')

    return render(request, "home.html", {'todos': todos, 'sort_by': sort_by})

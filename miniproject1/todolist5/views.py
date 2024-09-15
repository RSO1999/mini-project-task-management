from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import TodoItem  # Import the TodoItem model
from django.http import HttpResponseRedirect
from .forms import TodoItemForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView
from django.views import View

# Create your views here.


def home(request):
    todos = TodoItem.objects.all()
    return render(request, "home.html", {'todos': todos})

    #if request.user.is_authenticated:
     #   todos = TodoItem.objects.filter(user=request.user).order_by('due_date')
    #else:
    #    todos = []
    
    #return render(request, 'home.html', {'todos': todos})

class AddTodoItemView(FormView):
    template_name = 'add_todo_item.html'  # The template for displaying the form
    form_class = TodoItemForm # The form to use
    success_url = reverse_lazy('home')  # URL to redirect to after successful form submission

    # Override form_valid method to save the form and assign the user
    def form_valid(self, form):
        todo_item = form.save(commit=False)  # Do not commit yet
        if self.request.user.is_authenticated:
            todo_item.user = self.request.user  # Assign the logged-in user
        todo_item.save()  # Now save the object
        return super().form_valid(form)  # Continue with the default behavior

def delete_todo_item(request):
    todo_items = TodoItem.objects.all()
    return render(request, 'deleteTodo.html', {'todo_items': todo_items})

class BulkDeleteTodoView(View):
    #template_name = 'confirmDelete.html'
    success_url = reverse_lazy('delete_todo_item')

    def post(self,request, *args, **kwargs):
        selected_items = request.POST.getlist('todo_ids')
        if selected_items:
            TodoItem.objects.filter(id__in=selected_items).delete()

        return redirect(self.success_url)
        
        return render(request, self.template_name, {'todo_ids': selected_items})
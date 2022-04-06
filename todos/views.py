from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Todo

# Create your views here.

@login_required
def create(request):
    description = request.POST.get("description")
    todo = Todo()
    todo.owner = request.user
    todo.description = description
    todo.done = False
    todo.save()
    return redirect("/todos")

@login_required
def index(request):
    own_todos = Todo.objects.filter(owner=request.user)
    assigned_todos = Todo.objects.filter(assigned_to=request.user)
    return render(request, 'pages/index.html', {'own_todos': own_todos, 'assigned_todos': assigned_todos})

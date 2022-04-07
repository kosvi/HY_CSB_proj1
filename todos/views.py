from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Todo

# Create your views here.

@login_required
def create(request):
    description = request.POST.get("description")
    to = request.POST.get("assign_to")
    todo = Todo()
    todo.owner = request.user
    todo.assigned_to = User.objects.get(username=to)
    todo.description = description
    todo.done = False
    todo.save()
    return redirect("/todos")

@login_required
def update_status(request):
    todo = Todo.objects.get(pk=request.GET.get('todo'))
    todo.done = not todo.done
    todo.save()
    return redirect("/todos")

@login_required
def get_todo(request):
    todo = Todo.objects.get(pk=request.GET.get('id'))
    return JsonResponse({'id': todo.id, 'assigned_to': todo.assigned_to.username, 'description': todo.description, 'done': todo.done})

@login_required
def index(request):
    own_todos = Todo.objects.filter(owner=request.user)
    assigned_todos = Todo.objects.filter(assigned_to=request.user)
    # users = User.objects.exclude(username=request.user)
    users = User.objects.all()
    return render(request, 'pages/index.html', {'own_todos': own_todos, 'assigned_todos': assigned_todos, 'users': users})

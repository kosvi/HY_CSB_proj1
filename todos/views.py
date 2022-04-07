from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Todo
from .helpers import add_todo

# Create your views here.

ALLOW_SQL_INJECTION = True

@login_required
def create(request):
    description = request.POST.get("description")
    to = request.POST.get("assign_to")
    assigned_to = User.objects.get(username=to)
    if ALLOW_SQL_INJECTION:
        add_todo(request.user.id, assigned_to.id, description)
    else:
        todo = Todo()
        todo.owner = request.user
        todo.assigned_to = assigned_to
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
def update_todo(request):
    todo = Todo.objects.get(pk=request.POST.get('id'))
    todo.assigned_to = User.objects.get(username=request.POST.get('assign_to'))
    todo.description = request.POST.get('description')
    todo.save()
    return redirect("/todos")

@csrf_exempt
@login_required
def delete_todo(request):
    todo = Todo.objects.get(pk=request.POST.get('id'))
    todo.delete()
    return redirect("/todos")

@login_required
def get_todo(request):
    try:
        todo = Todo.objects.get(pk=request.GET.get('id'))
    except Todo.DoesNotExist:
        todo = None
    finally:
        id = todo.id if todo else 0
        assigned_to = todo.assigned_to.username if todo and todo.assigned_to else "null"
        description = todo.description if todo else ""
        done = True if todo else False
        return JsonResponse({'id': id, 'assigned_to': assigned_to, 'description': description, 'done': done, })
        # return JsonResponse({'id': todo.id, 'assigned_to': todo.assigned_to.username, 'description': todo.description, 'done': todo.done})

@login_required
def index(request):
    own_todos = Todo.objects.filter(owner=request.user)
    assigned_todos = Todo.objects.filter(assigned_to=request.user)
    # users = User.objects.exclude(username=request.user)
    users = User.objects.all()
    return render(request, 'pages/index.html', {'own_todos': own_todos, 'assigned_todos': assigned_todos, 'users': users})

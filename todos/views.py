from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Todo
from .helpers import add_todo, reset_db

# Create your views here.

# This function creates new todos. There is an if ... else statement here
#
# Depending on the value of ALLOW_SQL_INJECTION, this function eiher uses
# our programmer clonky function that gets the job done but has some serious
# flaws or uses ORM to achieve the same result but with a bit safer manner
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
    if todo.assigned_to == request.user:
        todo.done = not todo.done
        todo.save()
    return redirect("/todos")

@login_required
def update_todo(request):
    todo = Todo.objects.get(pk=request.POST.get('id'))
    if todo.owner == request.user:
        todo.assigned_to = User.objects.get(username=request.POST.get('assign_to'))
        todo.description = request.POST.get('description')
        todo.save()
    return redirect("/todos")

# @csrf_exempt
@login_required
def delete_todo(request):
    todo = Todo.objects.get(pk=request.GET.get('id'))
    if todo.owner == request.user:
        todo.delete()
    return redirect("/todos")

# This function servers todos in JSON-format for the script that manages todo-editing
@login_required
def get_todo(request):
    # The problem here is that while we do require login in order to use the API
    # we don't really check WHO the logged in user is. That is, any logged in user
    # can read any todo by simply guessing the ID
    try:
        todo = Todo.objects.get(pk=request.GET.get('id'))
        # A simple way to fix the issues is to check the owner of the todo 
        # and make sure it matches the user making the request. If not, 
        # just set to todo to null unless you want to be fair and provide 403 or something
        # if not todo.owner == request.user:
        #     todo = None
    except Todo.DoesNotExist:
        todo = None
    finally:
        id = todo.id if todo else 0
        owner = todo.owner.username if todo and todo.owner else "null"
        assigned_to = todo.assigned_to.username if todo and todo.assigned_to else "null"
        description = todo.description if todo else ""
        done = True if todo else False
        return JsonResponse({'id': id, 'owner': owner, 'assigned_to': assigned_to, 'description': description, 'done': done, })

# This is our index-page where todos are listed
# Todos are listed in two separate categories: todos user has created and todos assigned to the user (same todo can be in both categories!)
@login_required
def index(request):
    own_todos = Todo.objects.filter(owner=request.user)
    assigned_todos = Todo.objects.filter(assigned_to=request.user)
    users = User.objects.all()
    return render(request, 'pages/index.html', {'own_todos': own_todos, 'assigned_todos': assigned_todos, 'users': users})



# This is just to allow resetting of db
def reset_db_endpoint(request):
    reset_db()
    return redirect("/todos")
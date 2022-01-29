from .models import * 
from django.shortcuts import render
from django.shortcuts import redirect

def list_todos(request):
    if request.method == "GET":
        todos = Todo.objects.all().order_by('-id')
        context = {
            'todos': todos
        }
        return render(request, "app/todo.html", context)
    

def detailed_todos(request,pk):
    cur_todo = Todo.objects.get(pk = pk)
    context = {
        'todo': cur_todo
    }
    return render(request, "app/todo_detail.html", context)

def create_todo(request):
    if request.method == "POST":
        new_todo = Todo.objects.create(
            title = request.POST.get('todo_title'),
            user =  request.user,
            description = request.POST.get('todo_description'),
            deadline_time = request.POST.get('todo_deadline'),
            priority = request.POST.get('todo_priority'),
            status =0,
        )
        new_todo.save()
    return redirect("/todo")

def edit_todo(request, id):
    new_todo = Todo.objects.get(id=id)
    if request.method == "GET":
        context = {
            'todo': new_todo
        }
        return render(request, "app/todo_edit.html", context)

    elif request.method == "POST":
        new_todo.title = request.POST.get('todo_title'),
        new_todo.user =  request.user,
        new_todo.description = request.POST.get('todo_description'),
        new_todo.deadline_time = request.POST.get('todo_deadline'),
        new_todo.priority = request.POST.get('todo_priority'),
        # new_todo.status = request.POST.get('todo_priority'),
        new_todo.save()
        return redirect("/todo_detail/"+str(id))


def handle_todo_done(request,pk):

    if request.method == "POST":
        todo_id = pk
        cur_todo = Todo.objects.get(id = todo_id)
        cur_todo.status = 1 if cur_todo.status == 0 else 0
        cur_todo.save()
    return redirect("/todo")
    
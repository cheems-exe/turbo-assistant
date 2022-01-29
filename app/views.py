from django.shortcuts import render
from .models import WorkEfficiency
from datetime import date
from django.db.models import Q
from django.shortcuts import redirect
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout
import os
from glob import glob
import torch
from django.core.files.storage import default_storage
from django.shortcuts import render
import requests


def login_user(request):
    # return render(request, 'epapp/login.html')
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,"Wrong credentials,Please try again !")
            return redirect('/login/')
    else:
        return render(request, 'app/login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            name = name.split(' ')
            user = User.objects.create_user(username, email, password)
            # user.save()
            user.first_name=name[0]
            try:
                user.last_name=name[1]
            except:
                user.last_name=''
            user.save()
        except Exception as e:
            messages.error(request,e)
        return redirect('/login/')
    else:
        return render(request, 'app/signup.html')

def signout(request):
	logout(request)
	messages.success(request,'Successfully logged out')
	return redirect('/login/')


def home(request):
    if request.method == "GET":
        return render(request, 'app/home.html')
    raise Http404('No such request')


def journal(request):
    if request.method == "GET":
        journal_objects = JournalPage.objects.filter(user=request.user).order_by('date')

        return render(request, "app/journal_list.html", {"journals": journal_objects})

    elif request.method == "POST":
        todays_entry = JournalPage.objects.filter(user=request.user, date=datetime.datetime.today())
        if todays_entry:
            messages.error(request, "Already entered today's data")
            return redirect("journal")

        else:
            rating = request.POST.get("day_rating")
            desc = request.POST.get("day_description")

            todays_entry = JournalPage(
                user=request.user,
                date=datetime.datetime.today(),
                day_rating=rating,
                day_description=desc)
            todays_entry.save()

            messages.success(request, "Entered today's data successfully")
            return redirect("journal")

    else:
        raise Http404('No such request')


def detailed_journal(request, id):
    obj = JournalPage.objects.get(id=id)
    return render(request, "app/journal_detail.html", {"journal": obj, "range": range(obj.day_rating)})


def health(request):
    return render(request, "app/health.html")


def meditation(request):
    if request.method == 'POST':
        print(request.POST)
        activity = Activity(user=request.user, activity_name="MEDITATION", date=datetime.datetime.now())
        activity.save()

    return render(request, "app/meditation.html")


def relaxing_sounds(request):
    return render(request, "app/relaxing_sounds.html")


@login_required
def list_todos(request):
    if request.method == "GET":
        """
            
        """
        todos = Todo.objects.filter(user = request.user)
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



def start_pomodoro_timer(request):
    context = {
        'is_break' : "False",
        "time": "10"
    }
    print("inside start pomodoro")
    return render(request, "app/pomodoro_timer.html",context)
    

def break_session(request):
    print("inside break_session")
    today = date.today()
    work_obj = WorkEfficiency.objects.filter(user= request.user, date = today).first()
    context = {
        'is_break' : True,
        "time": "04"
    }
    if work_obj is None:
        work_obj = WorkEfficiency.objects.create(
            user = request.user,
            date = today,
            pomodoro_cycles = 0,
        )

    work_obj.pomodoro_cycles += 1
    work_obj.save()
    # return redirect("/pomodoro")
    return render(request, "app/pomodoro_timer.html",context)


def play_games(reqest):
    return render(reqest, "app/play_games.html")


def text_summarizer(text):
    print(text)

    url = "https://text-analysis12.p.rapidapi.com/summarize-text/api/v1.1"

    payload = "{\r\n    \"language\": \"english\",\r\n    \"summary_percent\": 10,\r\n    \"text\":" + text + "\r\n}"
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "text-analysis12.p.rapidapi.com",
        'x-rapidapi-key': "8e6fb730b6mshd2d435403413191p1f0308jsn3fce5bdcbc52"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text


def speech_to_text(request):
    if request.method == 'POST':
        print(request.POST)
        device = torch.device('cpu')
        model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_stt', language='en', device=device)
        (read_batch, split_into_batches, read_audio, prepare_model_input) = utils
        # os.save()

        file = request.FILES['sound']
        file_name = default_storage.save(file.name, file)
        print("Saved", os.getcwd())
        print("Hellooooo", os.path.join(os.getcwd(), f"media\\{file_name}"))

        file_path = os.path.join(os.getcwd(), f"media\\{file_name}")
        test_file = glob(file_path) 
        print('HERE', test_file)

        batches = split_into_batches(test_file, batch_size=10)

        input_to_the_model = prepare_model_input(read_batch(batches[0]), device=device)

        output = model(input_to_the_model)
        transcribed_text = ""
        for example in output:
            transcribed_text = decoder(example.cpu())

        os.remove(file_path)
        return render(request, "app/text_summarizing.html",{"summarized_text": transcribed_text})

    return render(request, "app/text_summarizing.html",{"summarized_text": ""})

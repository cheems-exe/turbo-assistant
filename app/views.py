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
import json
import random
import sklearn
import pickle
import pandas as pd


with open("ml_utils/food_data.json") as f:
    food_data = json.load(f)
with open("ml_utils/food_recommendation.pkl", "rb") as f:
    model = pickle.load(f)
df = pd.read_csv("ml_utils/food_recommendation.csv")
names = list(df["name"].copy())
features = df.drop(["name"], axis=1)


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

def dashboard(request):
    user=request.user
    todos = Todo.objects.filter(user = request.user)[:6]
    pomodoro = WorkEfficiency.objects.filter(user=user)
    e_date = []
    e_data = []
    for i in pomodoro:
        e_date.append(str(i.date)[:10])
        e_data.append(i.pomodoro_cycles)
    pomodoro_dict ={ 'date':e_date, 'data':e_data }
    context={'todos':todos, 'pompdoro_dict':json.dumps(pomodoro_dict) }
    return render(request, 'app/dashboard.html',context)

@login_required
def home(request):
    if request.method == "GET":
        return redirect('/dashboard')
        # return render(request, 'app/index.html')
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
        cur_todo.status = (cur_todo.status +1)%2
        cur_todo.save()
    return redirect("/todo/"+str(pk))


def start_pomodoro_timer(request):
    context = {
        'is_break' : "False",
        "min": "00",
        "sec": "10",
        "what": "WORK"
    }
    # messages.success(request, "Break complete! Back to work :)")
    return render(request, "app/pomodoro_timer.html",context)


def break_session(request):
    print("inside break_session")
    today = date.today()
    work_obj = WorkEfficiency.objects.filter(user= request.user, date = today).first()
    context = {
        'is_break' : True,
        "min": "00",
        "sec": "04",
        "what": "BREAK"
    }
    # messages.success(request, "Work completed! Enjoy a break.")
    if work_obj is None:
        work_obj = WorkEfficiency.objects.create(
            user = request.user,
            date = today,
            pomodoro_cycles = 0,
        )

    work_obj.pomodoro_cycles += 1
    work_obj.save()

    # take a gap in the cycles
    if work_obj.pomodoro_cycles%2 == 0:
        return redirect("/break_page")
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


def charts(request):
    user=request.user
    journal = JournalPage.objects.filter(user=user)
    activity = Activity.objects.filter(user=user)
    pomodoro = WorkEfficiency.objects.filter(user=user)
    j_date = []
    j_data = []
    a_date = []
    a_data = []
    e_date = []
    e_data = []
    for i in journal:
        j_date.append(str(i.date))
        j_data.append(i.day_rating)


    for i in activity:
        a_date.append(str(i.date))
        # a_data.append(i.date)

    for i in pomodoro:
        e_date.append(str(i.date)[:10])
        e_data.append(i.pomodoro_cycles)
    journal_dict ={ 'date':j_date, 'data':j_data }
    activity_dict ={ 'date':j_date, 'data':j_data }
    pomodoro_dict ={ 'date':e_date, 'data':e_data }
    print({'journal_dict':journal_dict,'activity_dict':activity_dict,'pompdoro_dict':pomodoro_dict})
    return render(request, "app/charts.html", {'journal_dict':json.dumps(journal_dict),'activity_dict':json.dumps(activity_dict),'pompdoro_dict':json.dumps(pomodoro_dict)} )


def break_page(request):
    return render(request,"app/break_page.html")


def music(request):
    #youtube-dl --dump-json --flat-playlist "https://www.youtube.com/watch?v=kXYiU_JCYtU&list=PL6Lt9p1lIRZ311J9ZHuzkR5A3xesae2pk" | jq -r '"\(.title)\nhttps://youtu.be/\(.id)\n"'
    all_categories = [
        "Rock",
        "EDM",
        "Jazz",
        "Pop",
        "Motivation",
        "Country",
        "Hindi",
    ]

    all_categories_songs = {
        "Rock":[
            "https://youtu.be/kXYiU_JCYtU",
            "https://youtu.be/eVTXPUF4Oz4",
            "https://youtu.be/3YxaaGgTQYM",
            "https://youtu.be/YlUKcNNmywk",
            "https://youtu.be/7QU1nvuxaMA",
            "https://youtu.be/fV4DiAyExN0",
            "https://youtu.be/kPBzTxZQG5Q",
            "https://youtu.be/yKNxeF4KMsY",
            "https://youtu.be/rn_YodiJO6k",
            "https://youtu.be/8sgycukafqQ",
            "https://youtu.be/1cQh1ccqu8M",
            "https://youtu.be/k4V3Mo61fJM",
            "https://youtu.be/SBjQ9tuuTJQ",
            "https://youtu.be/iAP9AF6DCu4",
            "https://youtu.be/gGdGFtwCNBE",
            "https://youtu.be/0J2QdDbelmY",
            "https://youtu.be/98Akpf1ph2o",
            "https://youtu.be/RF0HhrwIwp0",
        ],
        "EDM":[
            "https://youtu.be/60ItHLz5WEA",
            "https://youtu.be/YqeW9_5kURI",
            "https://youtu.be/0zGcUoRlhmw",
            "https://youtu.be/papuvlVeZg8",
            "https://youtu.be/uHVQChDSwx0",
            "https://youtu.be/kOkQ4T5WO9E",
            "https://youtu.be/IcrbM1l_BoI",
            "https://youtu.be/FM7MFYoylVs",
            "https://youtu.be/JRfuAukYTKg",
            "https://youtu.be/v8TVixpaBcQ",
            "https://youtu.be/IPYTxAHeR_o",
            "https://youtu.be/uO59tfQ2TbA",
            "https://youtu.be/ebXbLfLACGM",
            "https://youtu.be/foE1mO2yM04",
            "https://youtu.be/cNGJ1bf8XUU",
            "https://youtu.be/nntGTK2Fhb0",
            "https://youtu.be/L8eRzOYhLuw",
        ],
        "Jazz":[
           "https://youtu.be/ZZcuSBouhVA",
            "https://youtu.be/vmDDOFXSgAs",
            "https://youtu.be/ZrfzenYhv9w",
            "https://youtu.be/CWeXOm49kE0",
            "https://youtu.be/qJi03NqXfk8",
            "https://youtu.be/qWG2dsXV5HI",
            "https://youtu.be/WqEweV0eScg",
            "https://youtu.be/TDETNk20Vkc",
            "https://youtu.be/xISaCzXYYg8",
            "https://youtu.be/N76ErzOdk9g",
            "https://youtu.be/zGsGwFBoEgc",
            "https://youtu.be/HmroWIcCNUI",
            "https://youtu.be/ujChUYkPvec",
            "https://youtu.be/h6NCx0wcrC4",
            "https://youtu.be/ECw3WAX41OA",
            "https://youtu.be/I777BcgQL9o",
            "https://youtu.be/yXK0pZx92MU",
            "https://youtu.be/jUN01HYwRX4",
            "https://youtu.be/KsAf0ra6Vd4",
        ],
        "Pop":[
           "https://youtu.be/OPf0YbXqDm0",
            "https://youtu.be/JGwWNGJdvx8",
            "https://youtu.be/rYEDA3JcQqw",
            "https://youtu.be/qod03PVTLqk",
            "https://youtu.be/kTJczUoc26U",
            "https://youtu.be/N-4YMlihRf4",
            "https://youtu.be/2Vv-BfVoq4g",
            "https://youtu.be/h3h035Eyz5A",
            "https://youtu.be/09R8_2nJtjg",
            "https://youtu.be/v8TVixpaBcQ",
            "https://youtu.be/bo_efYhYU2A",
            "https://youtu.be/tt2k8PGm-TI",
            "https://youtu.be/SVQwO0nfb08",
            "https://youtu.be/k2qgadSvNyU",
            "https://youtu.be/X-yIEMduRXk",
            "https://youtu.be/fIjXcERE32A",
            "https://youtu.be/fLexgOxsZu0",
            "https://youtu.be/aJOTlE1K90k",
            "https://youtu.be/g0CDGknfAto",
            "https://youtu.be/RdVx-GrnQzk",
        ],
        "Motivation":[
          "https://youtu.be/hT_nvWreIhg",
            "https://youtu.be/1G4isv_Fylg",
            "https://youtu.be/sENM2wA_FTg",
            "https://youtu.be/Sv6dMFF_yts",
            "https://youtu.be/dqUdI4AIDF0",
            "https://youtu.be/8aRor905cCw",
            "https://youtu.be/gGdGFtwCNBE",
            "https://youtu.be/Qt2mbGP6vFI",
            "https://youtu.be/w5tWYmIOWGk",
            "https://youtu.be/a5uQMwRMHcs",
            "https://youtu.be/LKaXY4IdZ40",
            "https://youtu.be/jZhQOvvV45w",
            "https://youtu.be/co6WMzDOh1o",
            "https://youtu.be/dvgZkm1xWPE",
            "https://youtu.be/jFg_8u87zT0",
            "https://youtu.be/RFS5N_yAGTo",
            "https://youtu.be/F3EG4olrFjY",
        ],
        "Country":[
            "https://youtu.be/kXYiU_JCYtU",
            "https://youtu.be/eVTXPUF4Oz4",
            "https://youtu.be/3YxaaGgTQYM",
            "https://youtu.be/YlUKcNNmywk",
            "https://youtu.be/7QU1nvuxaMA",
            "https://youtu.be/fV4DiAyExN0",
            "https://youtu.be/kPBzTxZQG5Q",
            "https://youtu.be/yKNxeF4KMsY",
            "https://youtu.be/rn_YodiJO6k",
            "https://youtu.be/Soa3gO7tL",
            "https://youtu.be/HyHNuVaZJ",
            "https://youtu.be/8sgycukafqQ",
            "https://youtu.be/1cQh1ccqu8M",
            "https://youtu.be/k4V3Mo61fJM",
            "https://youtu.be/SBjQ9tuuTJQ",
            "https://youtu.be/iAP9AF6DCu4",
            "https://youtu.be/gGdGFtwCNBE",
            "https://youtu.be/0J2QdDbelmY",
            "https://youtu.be/98Akpf1ph2o",
            "https://youtu.be/RF0HhrwIwp0",
        ],
        "Hindi":[
            "https://youtu.be/Ps4aVpIESkc",
            "https://youtu.be/IJq0yyWug1k",
            "https://youtu.be/MRtRcTfszjY",
            "https://youtu.be/PVxc5mIHVuQ",
            "https://youtu.be/92J9p0VplTo",
            "https://youtu.be/Ydp5fLbxUbk",
            "https://youtu.be/hejXc_FSYb8",
            "https://youtu.be/yFZvQ1Uv358",
            "https://youtu.be/Dp6lbdoprZ0",
            "https://youtu.be/3KXZduvOfDo",
            "https://youtu.be/NzpkclSyDNs",
            "https://youtu.be/fWQpb6T89d4",
            "https://youtu.be/RemShT6JAHw",
            "https://youtu.be/ucMJu94UpTM",
            "https://youtu.be/xRb8hxwN5zc",
            "https://youtu.be/xitd9mEZIHk",
            "https://youtu.be/BTRPBiE_1lA",
            "https://youtu.be/mt9xg0mmt28",
            "https://youtu.be/hVCYwwFwGEE",
            "https://youtu.be/eHRrZ5DQCV4",
        ],
    }
    context = {

         'test': zip([
            cat[random.randint(0,len(cat)-1)] for cat in  all_categories_songs.values()
        ], all_categories),
    }

    return render(request,"app/music.html",context)

def food(request):
    x = ['Aloo Paratha', 'Appam', 'Bacon', 'Barfi', 'Bengan Bharta', 'Besan Ladoo', 'Bhel', 'Bhindi Masala', 'Bisi Bele Bath', 'Blueberry Pie', 'Brownie', 'Burritos', 'Butter Naan', 'Caramel Pudding', 'Chai', 'Chapati', 'Cheese Corn Balls', 'Chicken Hot Dog', 'Chicken Mexican Tacos', 'Chicken Noodles', 'Chicken Wings', 'Chimichanga', 'Chocolate Cupcake', 'Chocolate Fudge', 'Chole Bhature', 'Club Sandwich', 'Dal Bati', 'Dal Makhani', 'Dhokla', 'Donut', 'Egg Sandwich', 'Enchiladas', 'Falafel', 'Falooda', 'Fish Curry', 'Frankie', 'French Fries', 'Gajar Halwa', 'Garlic Bread', 'Gatte Ki Sabji', 'Ghevar', 'Gulab Jamun', 'Hara Bhara Kabab', 'Idli', 'Jain Biryani', 'Jain Fried Rice', 'Jain Hakka Noodles', 'Jain Pav Bhaji', 'Jalebi', 'Kadai Paneer', 'Kaju Katli', 'Kathi Roll', 'Kheer', 'Khichdi', 'Kulcha', 'Lasagna', 'Malai Kulfi', 'Malpua', 'Mango Pickle', 'Masala Dosa', 'Misal Pav', 'Momos', 'Mysore Pak', 'Nachos', 'Non Veg Biryani', 'Non Veg Burger', 'Non Veg Fried Rice', 'Non Veg Pizza', 'Omelet', 'Onion Rings', 'Pancakes', 'Paneer Wrap', 'Pani Puri', 'Pita Bread', 'Poha', 'Popcorn', 'Pumpkin Muffins', 'Puran Poli', 'Rabdi', 'Raita', 'Rajma', 'Rasgulla', 'Salsa Sauce', 'Samosa', 'Sarson Ka Saag', 'Sev Puri', 'Spaghetti', 'Steak', 'Strawberry Cake', 'Stuffed Potato', 'Sushi', 'Undhiyu', 'Upma', 'Vada Pav', 'Veg Biryani', 'Veg Burger', 'Veg Fried Rice', 'Veg Grilled Sandwich', 'Veg Hakka Noodles', 'Veg Hot Dog', 'Veg Kabab', 'Veg Pav Bhaji', 'Veg Pizza', 'Veg Pulav', 'Veg Spring Rolls', 'Vegetable Pakora', 'Vegetable Soup', 'Waffles', 'White Sauce Pasta']

    if request.method == "GET":
        # return render(request,"app/food.html",context)
        food_dataset = [i for i in food_data.values()]
        selected = []
        for _ in range(10):
            item = random.choice(food_dataset)
            selected.append(item)

        return render(request,"app/food.html", {"r_food": selected, "food_list": x})

    elif request.method == "POST":
        print(request.POST)
        d = dict(request.POST)
        spice = int(d["spice"][0])
        pref = int(d["pref"][0])
        food = [int(i) for i in d["food"]]

        feat = [0 for _ in range(len(list(features.iloc[0])))]
        for f in food:
            user_request = list(features.iloc[f])
            print(user_request)
            for i, val in enumerate(user_request):
                feat[i] += val

        feat[1] = spice
        feat[0] = pref

        rec = list()
        dist, ind = model.kneighbors([feat], n_neighbors=11)
        for i in ind[0][1:]:
            rec.append(x[i])

        res = []
        for name in rec:
            res.append(food_data[name])

        return render(request,"app/food.html", {"r_food": res, "food_list": x})

    else:
        raise Http404('No such request')

def food_detail(request,food_name):
    data = food_data[food_name]

    return render(request,'app/food_detail.html', {"food": data})

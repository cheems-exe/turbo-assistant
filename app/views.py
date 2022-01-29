# from django.http import HttpResponse
import datetime
import json
from django.contrib import messages

from django.contrib.auth.models import User
# push notif
from django.http.response import Http404, HttpResponse, JsonResponse
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST


from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout

# @require_GET
# def home2(request):
#     return HttpResponse('<h1>Home Page<h1>')
#
#
# @require_POST
# @csrf_exempt
# def send_push(request):
#     try:
#         body = request.body
#         data = json.loads(body)
#
#         if 'head' not in data or 'body' not in data or 'id' not in data:
#             return JsonResponse(status=400, data={"message": "Invalid data format"})
#
#         user_id = data['id']
#         user = get_object_or_404(User, pk=user_id)
#         payload = {'head': data['head'], 'body': data['body']}
#
#         return JsonResponse(status=200, data={"message": "Web push successful"})
#     except TypeError:
#         return JsonResponse(status=500, data={"message": "An error occurred"})
#
#
# def list_todo(request):
#     journal = Todo.objects.all()
#
#
# def create_todo(request):
#     if request.method == "POST":
#         title = request.POST['title']
#         description = request.POST['description']
#         user = request.user
#         deadline_time = request.POST['deadline']
#         priority = request.POST['priority']
#
#
# # Create your views here.

def loginn(request):
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
        # isteacher = request.POST.get('isteacher')
        password = request.POST.get('password')
        # print(name,password,username,phnumber,isteacher, email=email)
        try:
            User.objects.create_user(username=username, password=password, email=email).save()
            # user_details = ModiUser(user=user2,phno=phnumber,teacher=isteacher=='teacher')
            # user_details.save()
            
        except Exception as e:
            messages.error(request,e)
        return redirect('/login/')

def signout(request):
	logout(request)
	messages.success(request,'Successfully logged out')
	return redirect('/login/')


def home(request):
    if request.method == "GET":
        print("HERE")
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

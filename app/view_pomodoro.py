from re import template
from typing import List
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import WorkEfficiency
from datetime import date
from django.db.models import Q
from django.shortcuts import redirect

# class EventListView(ListView):
#     model = WorkEfficiency
#     template_name = 'app/pomodoro_timer.html'

# class EventD

def start_pomodoro_timer(request):
    # if request.method == "GET":
    #     # start time 
    #     start_time = WorkEfficiency.objects.filter(user= request.user)
    #     context = {
    #         'start_time': start_time
    #     }
    return render(request, "app/pomodoro_timer.html")
    


def pomodoro_session(request):
    today = date.today()
    work_obj = WorkEfficiency.objects.filter(Q(user= request.user) & Q(date = today)).first()
    if work_obj is None:
        work_obj = WorkEfficiency.objects.create(
            user = request.user ,
            date = today,
            pomodoro_cycles = 0,
        )
    
    context = {
        'pomodoro_session' : work_obj.pomodoro_cycles,
    }

    return render(request, "app/pomodoro_timer.html", context=context)

def add_done_sesssion(request):
    
    today = date.today()
    work_obj = WorkEfficiency.objects.filter(Q(user= request.user) & Q(date = today)).first()

    if work_obj is None:
        work_obj = WorkEfficiency.objects.create(
            user = request.user ,
            date = today,
            pomodoro_cycles = 0,
        )
    # else:
    #     work_obj.first()
    
    work_obj.pomodoro_cycles += 1
    work_obj.save()
    return redirect("/pomodoro")


"""
POST: 
    when? 
        -> session end hoga tab 
        -> start time is, jab post req - 30 mins

"""
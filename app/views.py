from django.http.response import Http404
# from django.http import HttpResponse
import json

from django.contrib.auth.models import User
from django.http.response import Http404
# push notif
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
# from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import *


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
#     todos = Todo.objects.all()
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
# def home(request):
#     if request.method == "GET":
#         return render(request, 'app/home.html')
#     raise Http404('No such request')
#
# # djrs
# # celery -A turbo.celery worker --pool=solo -l info
# # celery -A turbo beat -l info
# # pip freeze > requirements.txt

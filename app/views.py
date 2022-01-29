from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
# from django.http import HttpResponse
from django.shortcuts import redirect, render
from .tasks import *
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json


# Create your views here.
def home(request):
    if request.method=="GET":
        return render(request, 'app/home.html')
    raise Http404('No such request')

# djrs
# celery -A turbo.celery worker --pool=solo -l info
# celery -A turbo beat -l info
# pip freeze > requirements.txt
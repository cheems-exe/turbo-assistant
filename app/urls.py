from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),

]

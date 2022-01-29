from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from . import views
from .utils_text_summarizing import speech_to_text

urlpatterns = [
    path('', views.home, name='home'),
    path('journal/', views.journal, name='journal'),
    path('summarize_text/', speech_to_text, name="summarize_text"),
    path('meditation/', views.meditation, name="meditation"),
]

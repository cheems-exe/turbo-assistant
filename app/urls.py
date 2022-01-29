from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .utils_text_summarizing import speech_to_text
from .views import *
# from .views_to_dos import *
# from .view_pomodoro import *

urlpatterns = [
    path("", views.home, name="home"),
    
    path('todo/', list_todos, name="todo"),
    path('todo/<int:pk>/', detailed_todos, name="detailed_todos"),
    path('new_todo', create_todo, name="create_todo"),
    path('edit_todo/<int:id>', edit_todo, name="edit_todo"),
    path('handle_todo_done/<int:pk>/', handle_todo_done, name="handle_todo_done"),
    
    path('journal/', views.journal, name='journal'),
    path('detailed_journal/<int:id>/', views.detailed_journal, name='detailed_journal'),
    
    path('summarize_text/', speech_to_text, name="summarize_text"),
    
    path('health/', views.health, name="health"),
    path('meditation/', views.meditation, name="meditation"),
    
    path('pomodoro/', start_pomodoro_timer, name="pomodoro"),
    path('add_done_session/', add_done_sesssion, name="add_done_session"),
    path('relaxing_sounds/', relaxing_sounds, name="relaxing_sounds"),
    path('play_games/', play_games, name="play_games"),
    
    path('logout/', views.signout, name="logout"),
    path('login/', views.login_user, name="login"),
    path('signup/', views.signup, name="signup"),
]

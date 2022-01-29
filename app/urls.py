from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    
    path('todo/', list_todos, name="todo"),
    path('todo/<int:pk>/', detailed_todos, name="detailed_todos"),
    path('new_todo', create_todo, name="create_todo"),
    path('edit_todo/<int:id>', edit_todo, name="edit_todo"),
    path('handle_todo_done/<int:pk>/', handle_todo_done, name="handle_todo_done"),
    
    path('journal/', journal, name='journal'),
    path('detailed_journal/<int:id>/', detailed_journal, name='detailed_journal'),
    
    path('summarize_text/', speech_to_text, name="summarize_text"),
    
    path('health/', health, name="health"),
    path('meditation/', meditation, name="meditation"),
    
    path('pomodoro/', start_pomodoro_timer, name="pomodoro"),
    path('break_session/', break_session, name="break_session"),
    path('relaxing_sounds/', relaxing_sounds, name="relaxing_sounds"),
    path('play_games/', play_games, name="play_games"),
    
    path('logout/', signout, name="logout"),
    path('login/', login_user, name="login"),
    path('signup/', signup, name="signup"),
]

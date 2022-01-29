from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
from .utils_text_summarizing import speech_to_text

# webpush
from django.urls import path, include
from .views import *
from .views_to_dos import * 
urlpatterns = [
    # path('', views.home, name='home'),
    # url(r'^webpush/', include('app.urls'))

    # webpush
    # path('admin/', admin.site.urls),
    # path('h2', home2),
    # path('send_push', send_push),
    path('summarize_text/', speech_to_text),
    # path('webpush/', include('webpush.urls')),

    path('todo/',list_todos),
    path('todo/<int:pk>/', detailed_todos, name="detailed_todos"),
    path('new_todo', create_todo, name="create_todo"),
    path('edit_todo/<int:id>', edit_todo, name="edit_todo"),
    path('handle_todo_done/<int:pk>/', handle_todo_done, name="handle_todo_done"),

]

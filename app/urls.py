from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
from .utils_text_summarizing import speech_to_text

# webpush
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    # url(r'^webpush/', include('app.urls'))

    # webpush
    # path('admin/', admin.site.urls),
    # path('h2', home2),
    # path('send_push', send_push),
    path('summarize_text/', speech_to_text),
    # path('webpush/', include('webpush.urls')),

]

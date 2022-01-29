from django import forms
from .models import *


class TodoCreationForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['title', 'description', 'deadline_time', 'priority']

    # title = models.CharField(max_length=75)
    # description = models.TextField(max_length=500)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # deadline_time = models.DateTimeField()
    # priority = models.IntegerField(choices=PRIORITY_CHOICES)
    # status = models.IntegerField(default=0)

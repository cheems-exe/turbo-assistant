from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

class Todo(models.Model):
    PRIORITY_CHOICES = (
        (1, "High priority"),
        (2, "Medium priority"),
        (3, "Low priority"),
    )
    title = models.TextField(max_length=75)
    description = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline_time = models.DateTimeField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES)


class JournalPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(datetime.now) 
    day_rating = models.IntegerField(default=0)
    day_description = models.TextField()


class Activity(models.Model):
    """
        meditation 
        cooking 
        
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=100)
    date = models.DateTimeField(datetime.now)


class WorkEfficiency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pomodoro_cycles = models.IntegerField(default=0)
    date = models.DateTimeField(datetime.now)



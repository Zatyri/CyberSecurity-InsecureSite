from django.db import models

from django.contrib.auth.models import User

class TaskList(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  listName = models.CharField(max_length=200, default='no name') 

class Task(models.Model):
  list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
  task = models.CharField(max_length=200)  
  completed = models.BooleanField()

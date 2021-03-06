from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import TaskList, Task
import sqlite3


@login_required
@csrf_exempt
def index(request):
  if request.method == 'GET':
    if 'newList' in request.GET:
      name = request.GET['newList']
      user = request.user.username
      query = "INSERT INTO TaskList (user, name) VALUES (?, ?)"
      conn = sqlite3.connect('polls/tasks.sqlite3')
      cursor = conn.cursor()
      values = [user, name]
      cursor.execute(query, values)
      conn.commit()  
  query = "SELECT name, id FROM TaskList WHERE user=?"
  user = request.user.username
  conn = sqlite3.connect('polls/tasks.sqlite3')
  cursor = conn.cursor()
  values = [user]
  cursor.execute(query, values)
  lists = cursor.fetchall()  
  conn.commit()
  
  return render(request, 'index.html', {'lists':lists})

def list(request):
  if request.method == 'GET':
    
    if 'id' in request.GET:
      id = request.GET['id']  
      conn = sqlite3.connect('polls/tasks.sqlite3')
      cursor = conn.cursor()
      if 'newTask' in request.GET:      
        taskName = request.GET['newTask']        
        query = "INSERT INTO Task (list, TaskName) VALUES (?, ?)"
        values = [id, taskName]
        try:
          cursor.execute(query, values)
        except:
          print('No duplicates allowed')
        conn.commit()
      if 'task' in request.GET:
        if 'complete' in request.GET:
          taskID = request.GET['task']
          status = request.GET['complete']          
          if status == '0' or status == '1':            
            query = "UPDATE Task SET Complete = (?) WHERE id = (?)"
            values = [status, taskID]
            cursor.execute(query, values)
            conn.commit()
      
      query = "SELECT name, id FROM TaskList WHERE id = %s;" % (id)
      values = [id]
      cursor.execute(query)      
      listName = cursor.fetchall()      
      conn.commit()
      query = "SELECT TaskName, Complete, id FROM Task WHERE list = %s;" % (id)  
      #http://127.0.0.1:8000/list/?id=1%20OR%201=1 
      cursor.execute(query)
      tasks = cursor.fetchall()
      conn.commit()
      if len(listName) > 0:        
        return render(request, 'list.html', {'listName': listName[0][0], 'listID': listName[0][1], 'tasks': tasks},)
    
      
  return render(request, 'list.html', {'listName': 'List not found'})

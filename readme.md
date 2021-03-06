# Cyber security base 2021 – Project 1
## Insecure Site
## LINK: https://github.com/Zatyri/CyberSecurity-InsecureSite
## Installation instructions
Project is developed with Python 3.9.1 and Django framework, so you need those two installed.
Python installation instructions: https://www.python.org/about/gettingstarted/
Django installation instructions: https://docs.djangoproject.com/en/3.1/topics/install/
Clone the repository to your computer and run migrations (make sure you are in the same directory as the file manage.py (insecureSite)) in your console
```
$ python manage.py makemigrations
```
Then
```
$ python manage.py migrate   
```
Create a superuser with name and password (you can freely choose the name and password)
```
$ python manage.py createsuperuser
```
Run the server
```
$ python manage.py runserver
```
Log on to http://127.0.0.1:8000/admin/ and create at least one user. Name and password can be of your own choosing.
Access the site by accessing http://127.0.0.1:8000/ 
(Please note that default port is 8000. If the port is in use on your computer might the port be different)
## How the app works
The app is a simple to-do list where users can create multiple lists with multiple tasks. Tasks can be set as completed. The task lists are displayed on the homepage as links and when you click on them are the lists tasks shown. New lists can be created at the homepage and new tasks added to lists on the same page tasks are listed.
## Some info
This is my first ever Django site and I am not familiar with Python prior to this course. The site was done by the help of Djangos getting started tutorial and other tutorials. Apologies for funky and spaghetti code and syntax.

## FLAW 1: Injection
Link: https://github.com/Zatyri/CyberSecurity-InsecureSite/blob/main/insecureSite/polls/views.py#L61
Flaw: The site is vulnerable to SQL injection attacks when displaying tasks to a specific list. Displaying a list tasks uses GET. When clicking on the corresponding list link on the homepage is the lists id sent to /lists. By adding for example to the id “AND 1=1” will all tasks in the database be shown in the lists tasks. The attacker can then mark or unmark tasks not belonging to them as completed.
Fix: A simple fix would be to use variables in the query and not add them straight to the query. Changing %s to (?). There is already a values variable in the code that you then can add to the execution of the query. Note that this must be done on queries on line 61 and 66.

## FLAW 2: Broken Authentication
Link: https://github.com/Zatyri/CyberSecurity-InsecureSite/blob/main/insecureSite/polls/views.py#L35
Flaw: While a user is forced to login when accessing the homepage, has the login check been omitted on the list URL. This means that a attacker can write /list/?id=(desired list id) and access it without logging in. 
Fix:  The fix is an easy one. Django offers great and easy authentication system. Simply add @login_required before the view list. This will check if the user us logged in and redirect the user to the login page if not logged in.

## FLAW 3: Broken access control
Link: https://github.com/Zatyri/CyberSecurity-InsecureSite/blob/main/insecureSite/polls/views.py#L61
Flaw: When accessing the list page is the query for the desired list done only by list id. This means that a user can alter the GET request with any desired id and access any users list. The user is then able to add tasks to other users lists and change tasks complete status.
Fix: The query needs to be changed to consider the logged in user and make query based on that. I assume that you are doing this list in order and have changed the queries in flaw 1. The query should the look like “SELECT name, id FROM TaskList WHERE id =(?)” add to the query “AND User = (?)”. Then store the logged in users name in a variable. You can get the username with request.user.username. Then add the variable to the values list. This fix can also be used to fix flaw 2.

## FLAW 4: XSS
Link: https://github.com/Zatyri/CyberSecurity-InsecureSite/blob/main/insecureSite/polls/templates/list.html#L13
Flaw: This flaw can easily be exploited if flaws 1-3 are not fixed. It is possible to add script tags as a task. This way can an attacker run scripts when the user views tasks in a list. This can be especially exploitable if flaws 1-3 are not fixed. Try adding a tasks <script>alert(‘hacked!’)</script> and test it for yourself.
Fix: Django escapes malicious characters very efficiently and the developer has desired that task are displayed unmutated. Remove the ‘autoescape off’ feature on line 13 and 33 in file list.html.

## FLAW 5: Security misconfiguration
Link: https://github.com/Zatyri/CyberSecurity-InsecureSite/blob/main/insecureSite/insecureSite/settings.py#L30
Flaw: The developer has not changed the DEBUG status in settings.py. It is by default True and that leads to a very comprehensive stack trace in the browser if an error occurs. With this information is it easy for an attacker to study the sites functionality and check dependency versions. With this information can the attacker figure out other venues for attacks and exploit known vulnerabilities in a specific dependencies version.
Fix: The fix is an easy on. Change the DEBUG status in settings.py to False. Note that you have to modify the ALLOWED_HOSTS = [] as it is by default empty. To allow any host add ‘*’, but this can be a security risk in it self as it allows HTTP Host header attacks. In a real application would you add the sires uri, but while the site is running on your computer can you add ['.localhost', '127.0.0.1']

## Ending notes
As stated in the beginning was this the first Django site I have written, and I have no experience with Python. While this course focuses on improving application security, would I have to say that Django offers particularly good security off the shelf. Most security flaws done in this site are done by force as the normal way would not allow security breaches. Compared to JavaScript and React, of which I am more experienced would most of these vulnerabilities been easily implemented. 

# minidrive
upload any type of file and access it from anywhere
 
 on your system Django must be installed
 
 pip install django
 
 you have to create file in folder filesys/migrations/ __init__.py
 
 run command in your Base directory
 
 python manage.py makemigrations
 
 python manage.py migrate
 
 By default admin username and password is admin
 
 you can visit to admin pannel through 127.0.0.1:8000/admin
 
  In file filesys/views.py you have to enter your email and password
  def contact(request):
       #in this function you have to your mail detials
 
 run the development server by command 
 
 python manage.py runserver
 

 

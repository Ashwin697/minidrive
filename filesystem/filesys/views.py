from django.shortcuts import render,redirect ,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from .models import Filesystem ,Contact
import os
from django.core.files.storage import Storage

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST" :
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(desc)<5:
            messages.error(request,"please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(request,"Message  sent Sucessfully")

            #sending mail to update
            fromaddr = 'email'
            toaddrs  =  "to email"

            # Gmail Login
            username = 'your email id'
            password = 'password'
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.mime.base import MIMEBase

            msg = MIMEMultipart()
            msg['From'] = 'Your email id'
            msg['To'] = 'to email id'
            msg['Subject'] = f'From FileSystem {name}'

            body = f'''
            New Message from {name}
            Email : {email}
            Phone : {phone}
            Msg   : {desc}
            '''
            msg.attach(MIMEText(body,'plain'))
            text = msg.as_string()
            # Sending the mail  
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, text)
            print('sending mail .......')
            server.quit()
        
    return render(request, 'contact.html')

def file(request):
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        filename = request.POST.get('ename')
        ufile = request.FILES.get('files')
        if not filename:
            messages.error(request," Filename is Required")
        elif len(filename) < 5 :
            messages.error(request," Filename must be 5 char long...")
        elif len(filename) > 30:
            messages.error(request," Filename must be less than 30 char...")
        elif not ufile:
            messages.error(request," File is Required")
        elif ufile.size > 419430400:
            messages.error(request," File should not more than 400MB ")
        else:
            modified_name = change_name(ufile.name)
            data = ufile.read()
            file_root,file_ext = os.path.splitext(modified_name)
            fal = Storage.get_alternative_name(request,file_root,file_ext)
            # fl,ext = os.path.splitext(fal)
            p2 = f'./media/uploads/{fal}'
            print(p2)  
            f = Filesystem(user=user,file=p2,filename=filename)
            f.save()
            with open(p2,'w') as pd:
                pd.write(str(data))
            messages.success(request," file uploaded sucessfully ")
    return render(request, 'file.html')


def handlesignup(request):
    if request.method =='POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('signuppassword')
        cpassword = request.POST.get('cpassword')

        
        if not username:
            messages.error(request," Username Required")
        elif len(username) < 4:
            messages.error(request," Username must be under characters")
        elif User.objects.filter(username=username).exists():
            messages.error(request," Already User exist. Try Another username")
        elif not fname:
            messages.error(request," First Name Required !!")
        elif len(fname) < 3 or len(fname) > 10:
            messages.error(request,' First Name must be 4 char long or more')
        elif not lname:
            messages.error(request,' Last Name Required..')
        elif len(lname) < 4 or len(lname) > 10:
            messages.error(request,' Last Name must be 4 char long or more')
        elif len(email) < 5 or len(email) < 16:
            messages.error(request,'Email must be 5 char long')
        elif User.objects.filter(email=email).exists():
            messages.error(request," Email Already exist. Try Another Email")
        elif not password:
            messages.error(request," Password Required")
        elif not cpassword:
            messages.error(request," Confirm Password Required")
        elif len(password) < 6 or len(password) > 20:
            messages.error(request,' Password must be 6 char long')
        elif password != cpassword:
            messages.error(request," Password do not match")
            
        else:
            
            myuser = User.objects.create_user(username,email,password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request," Account has been sucessfully created")

        return redirect('/')
    else:
        return HttpResponse(request,'404')


def handlelogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request," Sucessfully Logged In")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect('/')


def handlelogout(request):
    # if request.method == 'POST':
    logout(request)
    messages.success(request," Sucessfully Logged Out")
    return redirect('/')

def store(request):
    user = request.user

    if user.is_authenticated:
        ef = Filesystem.objects.all().filter(user=user).order_by('date')
        paginator = Paginator(ef,7)
        page_number = request.GET.get('page')
        page_obj =paginator.get_page(page_number)
        context = {'page_obj': page_obj }
        return render(request,'store.html',context)
    return HttpResponse(request,"<h1>404</h1>")


# handling space in file name
def change_name(filename):
    s = f'{filename}'
    return s.replace(' ','_')

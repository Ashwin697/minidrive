from django.urls import path ,include
from . import views


urlpatterns = [

   
    path('',views.home,name='home'),
    path('store',views.store,name='store'),
    path('file',views.file,name='file'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('signup',views.handlesignup,name='handlesignup'),
    path('login',views.handlelogin,name='login'),
    path('logout',views.handlelogout,name='logout'),

]
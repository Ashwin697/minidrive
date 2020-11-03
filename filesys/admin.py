from django.contrib import admin
from .models import Contact , Filesystem 

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','desc')

class FilesystemAdmin(admin.ModelAdmin):
    list_display = ('user','filename','file')

admin.site.register(Filesystem,FilesystemAdmin)

admin.site.register(Contact , ContactAdmin)
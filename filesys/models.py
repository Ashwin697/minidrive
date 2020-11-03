from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here

class Filesystem(models.Model):
    date = models.DateTimeField(default=now)
    file = models.FilePathField(path='media/uploads/')
    filename = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.file

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    phone = models.CharField(max_length=70)
    desc = models.CharField(max_length=500)

    def __str__(self):
        return self.name
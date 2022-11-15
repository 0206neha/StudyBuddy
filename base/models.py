from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
# # Create your models here.

class User(AbstractUser):
    # name=models.CharField(max_length=200,null=True)
    # username=models.EmailField(unique=True,null=True)
    username=models.CharField(max_length=200,null=True,unique=True)
    email=models.EmailField(unique=True,null=True)

    bio=models.TextField(null=True)

    avatar=models.ImageField(null=True,default="avatar.svg")

    USERNAME_FIELD='username'
    REQUIRED_FIELDS=[]


class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True) #blank->it can be blank as well
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    updated=models.DateTimeField(auto_now=True)#takes time every time we save content
    created=models.DateTimeField(auto_now_add=True) #only when we create first or save first instance

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return self.name
    
    #when we add a model to database we have to make migration,which creates a file of sql commands
    # run ->python manage.py makemigrations and 0001_initial.py gets created ,run->python manage.py migrate and it goes to lates migration and applies migration


class Message(models.Model):    
    # room=models.ForeignKey(Room,on_delete=models.SET_NULL)#when parent is deleted all message of child becomes null
    user=models.ForeignKey(User,on_delete=models.CASCADE) #user can have many messages but message can have only one user
    room=models.ForeignKey(Room,on_delete=models.CASCADE)#when parent is deleted all message of children also deleted
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']
        
    def __str__(self):
        return self.body[0:50]

1



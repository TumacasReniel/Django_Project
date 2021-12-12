from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models.deletion import CASCADE

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


class MyUserManager(BaseUserManager):
    def create_user(self,department,status,first_name,last_name,email,username, password=None):
        if not username:
            raise ValueError("username is required")
        user=self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            status=status,
            department=department
        )
        user.set_password(password)

        # user.save(using=self._db)
        return user
    
    def create_agent(self,department,status,first_name,last_name,email,username, password=None):
        user=self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            status=status,
            department=department
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,password=None):
        user=self.model(
            username=username
        )
        user.set_password(password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=200,unique=True)
    status = models.CharField(max_length=150)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser =models.BooleanField(default=False)
    department = models.ForeignKey('ST_System.departments',on_delete=CASCADE,blank=True, null=True)
    profile_pic = models.ImageField(blank=True,null=True,upload_to="images/")


    USERNAME_FIELD ="username"

    REQUIRED_FIELDS = []

    objects = MyUserManager()


    def __str__(self):
        return self.username

    
    def has_perm(slef, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True



class agent_od(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    category = models.ForeignKey('ST_System.categories',on_delete=CASCADE)
    level= models.IntegerField(default=1)


 

    




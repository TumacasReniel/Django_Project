from colorfield.fields import ColorField 
from django.db import models

from django.contrib.auth import get_user_model

from notifications.models import Notification


# Create your models here.

class ticket_statuses(models.Model):
    COLOR_CHOICES = [
        ("#000000","black"),
        ("#FF0000","red"),
        ("#0000FF","blue"),
        ("#008000","green"),
        ("#FFFF00","yellow"),
        ("#FFA500","orange"),
        ("#800080","purple"),
    ]
    
    ticket_status_name = models.CharField(max_length=50)
    ticket_status_color = ColorField(choices=COLOR_CHOICES,default='black')

    def __str__(self):
        return self. ticket_status_name

class departments(models.Model):
    department_name = models.CharField(max_length=50)

    def __str__(self):
        return self.department_name

class categories(models.Model):
    department = models.ForeignKey(departments,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class sub_categories(models.Model):
    department = models.ForeignKey(departments,on_delete=models.CASCADE)
    category = models.ForeignKey(categories,on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.sub_category_name

class priorities(models.Model):
    PL_CHOICES = [
         ("1","Low"),
        ("2","Medium"),
        ("3","Higj"),
    ]
    priority_level = models.IntegerField(choices=PL_CHOICES,default=1)

    def __str__(self):
        return self.priority_name


class tickets(models.Model):
    #PL_CHOICES = [
    #     ("1","Low"),
    #    ("2","Medium"),
    #    ("3","High"),
    #]
     
    User = get_user_model()
    creator = models.ForeignKey(User,on_delete=models.CASCADE, related_name='creator')
    agent = models.ForeignKey(User,on_delete=models.CASCADE, related_name='agent',blank=True,null=True)
    department = models.ForeignKey(departments,on_delete=models.CASCADE)
    category = models.ForeignKey(categories,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(sub_categories,on_delete=models.CASCADE, blank=True, null=True)
    subject = models.CharField( max_length=200)
    description = models.CharField(max_length=255)
    priority = models.IntegerField(default=1)
    status =  models.ForeignKey(ticket_statuses,on_delete=models.CASCADE,blank=True,null=True)
    attach_file = models.FileField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    

class replies(models.Model):
    User = get_user_model()
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name='sender',blank=True,null=True)
    ticket = models.ForeignKey(tickets,on_delete=models.CASCADE)
    message = models.CharField( max_length=350)
    attach_file = models.FileField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add =True)

class accepted_tickets(models.Model):
    User = get_user_model()
    agent = models.ForeignKey(User,on_delete=models.CASCADE,related_name="actual_agent")
    invited_agent = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="invited_agent")
    ticket = models.ForeignKey(tickets,on_delete=models.CASCADE)
    accepted_date = models.DateTimeField(auto_now_add=True)






    
    





   


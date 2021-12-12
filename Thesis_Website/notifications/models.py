from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPES = ((1,'Accept'),(2,'Complete'),(3,'Reply'))
    User = get_user_model()

    ticket  =models.ForeignKey('ST_System.tickets', on_delete=models.CASCADE,blank=True,null=True)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='noti_from_user',blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='noti_to_user',blank=True,null=True)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=50,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
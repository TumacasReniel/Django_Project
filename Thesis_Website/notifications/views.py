from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Notification


# Create your views here.

def user_notifications(request):
    noti_count = None
    if request.user.is_authenticated:
        noti = Notification.objects.filter(user=request.user)
        all_noti_count= noti.count()
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()

    context ={
        "all_noti_count":all_noti_count,
        "noti_count":noti_count,
        "noti":noti
        }

    return render(request,'user-notifications.html',context)

def user_see_notification(request,pk):
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()

    all_noti_count= Notification.objects.filter(id=pk,user=request.user).count()
    noti = Notification.objects.get(id=pk)
    if Notification.objects.filter(id=pk,user=request.user, is_seen=False).update(is_seen=True):
        return redirect('user_see_notification', pk=pk)
    
    context ={
        "all_noti_count":all_noti_count,
        "noti_count":noti_count,
        "noti":noti
        }

    return render(request,'user-see-notification.html', context)

def user_delete_notification(request):
    if request.method == 'POST':
        noti_id =  request.POST['noti_id']
        noti = Notification.objects.get(id=noti_id)
        user=request.user
        Notification.objects.filter(id=noti.id,user=user).delete()
        return redirect('user_notifications')
    
    return render(request, 'user-see-notification.html')
    

def agent_notifications(request):
    noti_count = None
    if request.user.is_authenticated:
        noti = Notification.objects.filter(user=request.user)
        all_noti_count =  noti.count()
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()

    context ={
        "noti_count":noti_count,
        "noti":noti
        }

    return render(request,'agent-notifications.html',context)

def agent_see_notification(request,pk):
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()

    noti = Notification.objects.get(id=pk)
    if Notification.objects.filter(id=pk,user=request.user, is_seen=False).update(is_seen=True):
        return redirect('agent_see_notification', pk=pk)
    
    context ={
        "noti_count":noti_count,
        "noti":noti
        }

    return render(request,'agent-see-notification.html', context)

def agent_delete_notification(request):
    if request.method == 'POST':
        noti_id =  request.POST['noti_id']
        noti = Notification.objects.get(id=noti_id)
        user=request.user
        Notification.objects.filter(id=noti.id,user=user).delete()
        return redirect('agent_notifications')
    
    return render(request, 'user-see-notification.html')
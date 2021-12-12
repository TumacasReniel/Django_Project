import json
import requests
from typing import Text
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.forms.forms import Form
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect

from django.shortcuts import redirect, render

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from accounts.models import agent_od
from notifications.models import Notification

from .models import *
from .forms import *

from monkeylearn import MonkeyLearn



# Create your views here.

def index(request):
    return render(request,'index.html')
    
def admin_dashboard(request):
    User = get_user_model()
    users = User.objects.all()
    ticket = tickets.objects.all()
    ts = ticket_statuses.objects.all()
    dep = departments.objects.all()
    cat = categories.objects.all()
    sub_c = sub_categories.objects.all()
    priority = priorities.objects.all()


    all_user_count = users.count()
    tickets_count = ticket.count()
    ts_count = ts.count()
    dep_count = dep.count()
    all_cat_count = cat.count()
    all_subc_count = sub_c.count()
    cat_count = categories.objects.filter(department=request.user.department).count()
    subc_count = sub_categories.objects.filter(department=request.user.department).count()
    user_count = User.objects.filter(department=request.user.department).count()
    priority_count = priority.count()

    context = {
        "all_user_count":all_user_count,
        "all_subc_count": all_subc_count,
        "all_cat_count": all_cat_count,
        "tickets_count":tickets_count,
        "ts_count":ts_count,
        "dep_count":dep_count,
        "cat_count":cat_count,
        "subc_count":subc_count,
        "user_count":user_count,
        "priority_count":priority_count
    }
    return render(request,'admin-dashboard.html',context)

def admin_tickets(request):
    ticket = tickets.objects.all()
    ts = ticket_statuses.objects.all()
    at = accepted_tickets.objects.all()
    tickets_count = ticket.count()

    context={
        "ticket":ticket,
        "ts":ts,
        "at":at,
        "tickets_count":tickets_count
    }
    return render(request,'admin-tickets.html',context)

def admin_ticket_statuses(request): 
    ts = ticket_statuses.objects.all()
    ts_count = ts.count()
    return render(request,'admin-ticket-statuses.html', {"ts":ts, "ts_count":ts_count})

def add_ticket_status(request):
    if request.method == 'POST':
        ts = ticket_statuses()
        ts.ticket_status_name = request.POST['ticket_status_name']
        ts.ticket_status_color = request.POST['ticket_status_color']

        if ticket_statuses.objects.filter(ticket_status_name= ts.ticket_status_name).exists():
            return redirect('admin_ticket_statuses')
        elif ticket_statuses.objects.filter(ticket_status_color=ts.ticket_status_color).exists():
            return redirect('admin_ticket_statuses')
        else:
            ts.save()
            return redirect('admin_ticket_statuses')
    else:
        return render(request,'admin-ticket-statuses.html')


def admin_delete_ticket_status(request):
    if request.method == 'POST':
        ts = ticket_statuses.objects.get(id=request.POST['id'])
        ts.delete()
        return redirect('admin_ticket_statuses')

    return render(request, 'admin-ticket-statuses.html')

def admin_update_ticket_status(request):
    if request.method == 'POST':
        ts = ticket_statuses.objects.get(id=request.POST['id'])
        ts.ticket_status_name = request.POST['ticket_status_name']
        ts.ticket_status_color = request.POST['ticket_status_color']

        if ticket_statuses.objects.filter(ticket_status_name=ts.ticket_status_name).exists():
            print("same name")
            return redirect('admin_ticket_statuses')
        else:
            ticket_statuses.objects.filter(id=ts.id).update(ticket_status_name=ts.ticket_status_name,ticket_status_color=ts.ticket_status_color)
            return redirect('admin_ticket_statuses')
    else:
        print("di post")

    return render(request, 'admin-ticket-statuses.html')
        
def admin_departments(request):
    showall = departments.objects.all()
    return render(request,'admin-departments.html',{"data":showall})

def add_department(request):
    if request.method == 'POST':
        if(request.POST.get('department_name')):
            dep = departments()
            dep.department_name = request.POST.get('department_name')

            if departments.objects.filter(department_name=dep.department_name).exists():
                 return redirect('admin_categories') 
            else:
                dep.save()
                return redirect('admin_categories') 
        else:
            return render(request,'admin-categories.html')
    
    return render(request,'admin-categories.html')

def admin_delete_department(request):
    if request.method == 'POST':
        dep = departments.objects.get(id=request.POST['id'])
        dep.delete()
        return redirect('admin_categories')

    return render(request, 'admin-categpries.html')

def admin_update_department(request):
    if request.method == 'POST':
        dep = departments.objects.get(id=request.POST['id'])
        form = depForm(request.POST, instance=dep)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')

    return render(request, 'admin-categories.html')


def add_category(request):
    if request.method == 'POST':
        if request.POST.get('category_name'):
            cat = categories()
            cat.category_name = request.POST['category_name']
            cat.department = departments.objects.get(id=request.POST['id'])

            if categories.objects.filter(department=cat.department,category_name=cat.category_name).exists():
                return redirect('admin_categories')
            else:
                cat.save()
                return redirect('admin_categories')
        else:
            return render(request,'admin-categories.html')
    else:
        return render(request,'admin-categories.html')

def admin_delete_category(request):
    if request.method == 'POST':
        cat = categories.objects.get(id=request.POST['id'])
        cat.delete()
        return redirect('admin_categories')

    return render(request, 'admin-categories.html')

def admin_update_category(request):
    if request.method == 'POST':
        cat = categories.objects.get(id=request.POST['id'])
        form = catForm(request.POST,instance=cat)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
            
    return render(request, 'admin-categories.html',{"cat":cat})

def admin_categories(request):
    dep = departments.objects.all()
    cat = categories.objects.all()
    subc = sub_categories.objects.all()
   
    return render(request,'admin-categories.html',{"dep":dep,"cat":cat,"subc":subc})

def add_sub_category(request):
    if request.method == 'POST':
        sub_cat = sub_categories()
        sub_cat.sub_category_name = request.POST['sub_category_name']
        sub_cat.department= departments.objects.get(id=request.POST['dep_id'])
        sub_cat.category = categories.objects.get(id=request.POST['cat_id'])


        if sub_categories.objects.filter(department=sub_cat.department,category=sub_cat.category,sub_category_name=sub_cat.sub_category_name).exists():
                return redirect('admin_categories')
        else:
            sub_cat.save()
            return redirect('admin_categories')
    else:
        return render(request,'admin-category.html')

def admin_delete_sub_category(request):
    if request.method == 'POST':
        subc = sub_categories.objects.get(id=request.POST['id'])
        subc.delete()
        return redirect('admin_categories')

    return render(request, 'admin-categories.html')

def admin_update_sub_category(request):
    if request.method == 'POST':
        subc = sub_categories.objects.get(id=request.POST['id'])
        form = subcForm(request.POST, instance=subc)

        if form.is_valid():
            form.save()
            return redirect('admin_categories')
        else:
            print("di valid")
    return render(request, 'admin-categories.html',{"subc":subc})


def admin_agent_view_more(request,pk):
    User = get_user_model()
    agent = User.objects.get(id=pk)
    od =  agent_od.objects.get(user_id=agent.id)
    
    return render(request,'admin-agent-view-more.html',{"agent":agent , "od":od} )

def admin_admin_view_more(request,pk):
    User = get_user_model()
    admin = User.objects.get(id=pk)
    
    return render(request,'admin-admin-view-more.html',{"admin":admin})

def admin_user_view_more(request,pk):
    User = get_user_model()
    user = User.objects.get(id=pk)

    return render(request,'admin-user-view-more.html',{"user":user})

def admin_users(request):
    User = get_user_model()
    users = User.objects.filter(department=request.user.department).order_by('status')
    all_users =  User.objects.all().order_by('id')
    dep = departments.objects.all()
    cat = categories.objects.all()
    agent = agent_od.objects.all()

    user_count = users.count()
    all_users_count =  User.objects.all().count()

    context={
        "all_users_count":all_users_count,
        "all_users":all_users,
        "users":users,"cat":cat,
        "dep":dep,"agent":agent,
        "user_count":user_count
    }
    user_count = User.objects.filter(department=request.user.department).count()
    return render(request,'admin-users.html', context)

def admin_priorities(request):
    return render(request,'admin-priorities.html')


def admin_profile(request):
    noti_count = None
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()

    context ={
        "noti_count":noti_count,
    }
    return render(request,'admin-profile.html')


def agent_dashboard_one(request):
    if request.user.is_authenticated:
        ts = ticket_statuses.objects.all()
        noti = Notification.objects.filter(user=request.user)
        noti_count = None
    
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()
        total_ticket_count =  tickets.objects.filter(creator=request.user).count()
        pending_ticket_count =  tickets.objects.filter(status=1,creator=request.user).count()
        processing_ticket_count =  tickets.objects.filter(status_id=2,creator=request.user).count()
        resolved_ticket_count =  tickets.objects.filter(status_id=3,creator=request.user).count()
        # completed_ticket_count = tickets.objects.filter(status_id="Complete",creator=request.user).count()

    context ={
        "noti_count":noti_count,
        "noti":noti,
        "ts":ts,
        "total_ticket_count":total_ticket_count,
        "pending_ticket_count":pending_ticket_count,
        "processing_ticket_count":processing_ticket_count,
        "resolved_ticket_count":resolved_ticket_count,
        # "completed_ticket_count":completed_ticket_count
        }

    return render(request,'agent-dashboard-one.html',context)


def agent_dashboard_two(request):
    ts = ticket_statuses.objects.all()
    noti_count = None
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()

    context ={
        "noti_count":noti_count,
        "ts":ts
    }
    return render(request,'agent-dashboard-two.html',context)

def agent_mytickets(request):
    dep = departments.objects.all()
    cat = categories.objects.all()
    subc = sub_categories.objects.all()
    ticket = tickets.objects.all()
    reply = replies.objects.all()
    at = accepted_tickets.objects.all()

    noti_count = None
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()

    context ={
        "noti_count":noti_count,
        "dep":dep,
        "cat":cat, 
        "subc":subc, 
        "ticket":ticket,
        "reply":reply,
        "at":at
    }
    return render(request,'agent-mytickets.html',context)

def agent_accepted_tickets(request):
    dep = departments.objects.all()
    cat = categories.objects.all()
    subc = sub_categories.objects.all()
    ticket = tickets.objects.all()
    reply = replies.objects.all()
    at = accepted_tickets.objects.all() 
    
    noti_count = None
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()

    context= {
        "noti_count":noti_count,
        "dep":dep,
        "cat":cat, 
        "subc":subc, 
        "ticket":ticket,
        "reply":reply,
        "at":at
    }
    return render(request,'agent-accepted-tickets.html',context)

def view_ticket(request,pk):
    ticket = tickets.objects.get(id=pk)

    dep = departments.objects.all()
    cat = categories.objects.all()
    subc = sub_categories.objects.all()
    reply = replies.objects.all()
    at = accepted_tickets.objects.all() 

    noti_count = None
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()
        replies_count =  replies.objects.filter(ticket=ticket.id).count()

    context ={
        "replies_count":replies_count,
        "noti_count":noti_count,
        "dep":dep,
        "cat":cat, 
        "subc":subc, 
        "ticket":ticket,
        "reply":reply,
        "at":at
    }
    return render(request,'agent-view-ticket.html',context)

def agent_view_accepted_ticket(request,pk):
    User = get_user_model()
    ticket = tickets.objects.get(id=pk)

    dep = departments.objects.all()
    cat = categories.objects.all()
    subc = sub_categories.objects.all()
    reply = replies.objects.all()
    at = accepted_tickets.objects.all()

    noti_count = None
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()
        agent =  User.objects.filter(status="SUPPORT AGENT")
        replies_count =  replies.objects.filter(ticket=ticket.id).count()
    
    context={
        "replies_count":replies_count,
        "noti_count" : noti_count,
        "dep":dep,
        "cat":cat, 
        "subc":subc, 
        "ticket":ticket,
        "reply":reply,
        "agent":agent,
        "at":at
    }

    return render(request,'agent-view-accepted-ticket.html',context)


def create_ticket(request):
    if request.method == 'POST':
        User = get_user_model()
        ticket=tickets()
        ticket.creator = User.objects.get(id=request.POST['creator'])
        ticket.department = departments.objects.get(id=request.POST['department'])
        ticket.category = categories.objects.get(id=request.POST['category'])
        ticket.status = ticket_statuses.objects.get(ticket_status_name="Pending")

        if request.POST['sub_category'] != "":
            ticket.sub_category = sub_categories.objects.get(id=request.POST['sub_category'])

        if request.FILES.get('attach_file', False):
            ticket.attach_file = request.FILES['attach_file']

        ticket.subject = request.POST['subject']
        ticket.description = request.POST['description']
        #ticket.save()

        #return redirect('agent_mytickets')
        ml = MonkeyLearn('94973664dd807eb954224b000700a16b0136467d')
        data = ["It was good to use"]
        model_id = 'cl_Aiu8dfYF'
        result  = ml.classifiers.classify(model_id, data)
        #print(result[0].external_id)

        #[{'text': 'help me', 'external_id': None, 'error': False, 'classifications': [{'tag_name': 'Not Urgent', 'tag_id': 77712469, 'confidence': 1.0}]}]
        
       
        #print(result.body)
        return HttpResponse(result.body[0]['classifications'][0]['tag_name'])
    else:
        print("di post")
    return render(request,'agent-mytickets.html')

def accept_ticket(request):
    if request.method == 'POST':
        User = get_user_model()
        at = accepted_tickets()
        at.agent = User.objects.get(id=request.POST['agent'])
        at.ticket = tickets.objects.get(id=request.POST['id'])
        ticket = tickets.objects.get(id=request.POST['id'])
        ticket.status = ticket_statuses.objects.get(ticket_status_name="Processing")
        ticket.agent = at.agent
        ticket.save()
        
        noti = Notification()
        noti.ticket = at.ticket
        noti.sender = at.agent
        noti.user = at.ticket.creator
        noti.notification_type=1
        noti.text_preview = "Agent accepted your ticket"


        current_site = get_current_site(request)

        # load a template like get_template() 
        # and calls its render() method immediately.
        email_body = render_to_string('agent-accept-ticket-notification.html',{"agent":noti.sender,"recepient":noti.user,"ticket":noti.ticket,"domain": current_site.domain, })
        email_subject ='Agent accepted your ticket'
        
        email = EmailMessage(
            email_subject,  
            email_body,
            settings.EMAIL_HOST_USER,
            [noti.user.email]
        )

        email.fail_silently=False
        email.send()
        noti.save()
        at.save()
        
        return redirect('agent_tag_tickets')
    else:
        print("di post")
    return render(request,'agent-tag-tickets.html')

def agent_delete_ticket(request):
    if request.method == 'POST':
        ticket = tickets.objects.get(id=request.POST["id"])
        ticket.delete()
        return redirect("agent_mytickets")
        
    return render(request,'agent-mytickets.html')

def agent_add_reply_on_accepted_ticket(request):
    if request.method == 'POST':
        reply=replies()
        reply.sender = request.user 
        reply.ticket = tickets.objects.get(id=request.POST['ticket'])
        pk = reply.ticket_id
        reply.message = request.POST['reply_msg']

        if request.FILES.get('reply_attach_file', False):
            reply.attach_file = request.FILES['reply_attach_file']

        noti = Notification()
        noti.ticket = reply.ticket
        noti.sender = reply.sender
        noti.user = reply.ticket.creator
        noti.notification_type=3
        noti.text_preview = 'Agent replied to your ticket'

        if reply.sender.status == "SUPPORT AGENT":
            current_site = get_current_site(request)

            # load a template like get_template() 
            # and calls its render() method immediately.
            email_body = render_to_string('agent-reply-ticket-notification.html',{"sender":reply.sender,"ticket":reply.ticket,"domain": current_site.domain, })
            email_subject ='Agent replied to your ticket'
            
            email = EmailMessage(
                email_subject,  
                email_body,
                settings.EMAIL_HOST_USER,
                [reply.ticket.creator.email],
            )

            email.fail_silently=False
            email.send()
            
        noti.save()
        reply.save()
        print("reply created")
        return redirect('agent_view_accepted_ticket', pk=pk)

    return render(request,'agent-view-accepted-ticket.html')

def add_reply(request):
    if request.method == 'POST':
        reply=replies()
        reply.sender = request.user 
        reply.ticket = tickets.objects.get(id=request.POST['ticket'])
        ticket_creator_email = reply.ticket.creator.email
        pk = reply.ticket_id
        reply.message = request.POST['reply_msg']

        if request.FILES.get('reply_attach_file', False):
            reply.attach_file = request.FILES['reply_attach_file']

        noti = Notification()
        noti.ticket = reply.ticket
        noti.sender = reply.sender
        noti.user = reply.ticket.creator
        noti.notification_type=3
        noti.text_preview = 'User replied to his/her ticket'
        noti.save()
        
        current_site = get_current_site(request)
        # load a template like get_template() 
        # and calls its render() method immediately.
        email_body = render_to_string('user-reply-ticket-notification.html',{"sender":reply.sender,"ticket":reply.ticket,"domain": current_site.domain, })
        email_subject ='User replied to his/her ticket'
        
        email = EmailMessage(
            email_subject,  
            email_body,
            settings.EMAIL_HOST_USER,
            [reply.ticket.agent.email],
        ) 

        email.fail_silently=False
        email.send()
            
        reply.save()
        

        return redirect('view_ticket', pk=pk)

    return render(request,'agent-view-tickets.html')

def delete_reply(request):
    if request.method == 'POST':
        reply = replies.objects.get(id=request.POST["id"])
        pk = reply.ticket_id
        reply.delete()
        return redirect('view_ticket', pk=pk )

    return render(request,'agent-mytickets.html')
    
def ajax_load_categories(request):
    department_id = request.GET.get('department_id')
    cat = categories.objects.filter(department_id=department_id).all()
    return render(request, 'agent-load-categories.html', {'cat': cat})
    # return JsonResponse(list(category.values('id', 'name')), safe=False)

def ajax_load_sub_categories(request):
    category_id = request.GET.get('category_id')
    subc = sub_categories.objects.filter(category_id=category_id).all()
    return render(request, 'agent-load-sub-categories.html', {'subc': subc})
    # return JsonResponse(list(sub_category.values('id', 'name')), safe=False)

def agent_profile(request):  
    agent = agent_od.objects.all()
    return render(request,'agent-profile.html',{"agent":agent})

def agent_view_ticket(request):
    noti_count = None
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()
    context={
        "noti_count" : noti_count,
    }
    return render(request,'agent-view-ticket.html',context)

def agent_tag_tickets(request):
    dep = departments.objects.all()
    cat = categories.objects.all()
    subc = sub_categories.objects.all()
    ticket = tickets.objects.all()
       
    noti_count = None
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()
        agent = agent_od.objects.get(user=request.user)
    context={
        "noti_count" : noti_count,
        "dep":dep,"cat":cat, "subc":subc,"ticket":ticket,
        "agent":agent
    }
    return render(request,'agent-tag-tickets.html',context)

def agent_invite_agent(request):
    if request.method == "POST":
        User = get_user_model()
        invited_agent_id = request.POST.get('invited_agent')

        ticket = tickets.objects.get(id=request.POST['ticket_id'])
        print(ticket.id)
        accepted_tickets.objects.filter(ticket_id=ticket.id).update(invited_agent=invited_agent_id)
        return redirect('agent_view_accepted_ticket',pk=ticket.id)
    
    return render(request,'agent-tag-tickets.html')

def user_profile(request):
    noti_count = None
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()

    context = {
        "noti_count":noti_count
    }
    return render(request,'user-profile.html',context)

def user_dashboard(request):
    if request.user.is_authenticated:
        ts = ticket_statuses.objects.all()
        noti = Notification.objects.filter(user=request.user)
        noti_count = None
    
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()
        total_ticket_count =  tickets.objects.filter(creator=request.user).count()
        pending_ticket_count =  tickets.objects.filter(status=1,creator=request.user).count()
        processing_ticket_count =  tickets.objects.filter(status_id=2,creator=request.user).count()
        resolved_ticket_count =  tickets.objects.filter(status_id=3,creator=request.user).count()
        # completed_ticket_count = tickets.objects.filter(status_id="Complete",creator=request.user).count()

    context ={
        "noti_count":noti_count,
        "noti":noti,
        "ts":ts,
        "total_ticket_count":total_ticket_count,
        "pending_ticket_count":pending_ticket_count,
        "processing_ticket_count":processing_ticket_count,
        "resolved_ticket_count":resolved_ticket_count,
        # "completed_ticket_count":completed_ticket_count
        }

    return render(request,'user-dashboard.html',context)

def user_mytickets(request):
    dep = departments.objects.all()
    cat = categories.objects.all()
    subc = sub_categories.objects.all()
    ticket = tickets.objects.all()

    noti_count = None
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()


    context = {
        "dep":dep,
        "cat":cat, 
        "subc":subc,
        "ticket":ticket,
        "noti_count":noti_count
    }
    
    return render(request,'user-mytickets.html',context)



def user_view_ticket(request,pk):
    ticket = tickets.objects.get(id=pk)

    dep = departments.objects.all()
    cat = categories.objects.all()
    subc = sub_categories.objects.all()
    reply = replies.objects.all()

    return render(request,'agent-view-ticket.html',{"dep":dep,"cat":cat, "subc":subc, "ticket":ticket,"reply":reply})


def user_view_myticket(request,pk):
    ticket = tickets.objects.get(id=pk)

    dep = departments.objects.all()
    cat = categories.objects.all()
    subc = sub_categories.objects.all()
    reply = replies.objects.all()

    noti_count = None
    if request.user.is_authenticated:
        noti_count =  Notification.objects.filter(user=request.user,is_seen=False).count()

    context ={
        "noti_count":noti_count,
        "dep":dep,
        "cat":cat,
        "subc":subc,
        "ticket":ticket,
        "reply":reply
        }

    return render(request,'user-view-ticket.html',context)

def user_create_ticket(request):
    if request.method == 'POST':
        User = get_user_model()
        ticket=tickets()
        ticket.creator = User.objects.get(id=request.POST['creator'])
        ticket.department = departments.objects.get(id=request.POST['department'])
        ticket.category = categories.objects.get(id=request.POST['category'])
        ticket.status = ticket_statuses.objects.get(ticket_status_name="Pending")

        if request.POST['sub_category'] != "":
            ticket.sub_category = sub_categories.objects.get(id=request.POST['sub_category'])

        if request.FILES.get('attach_file', False):
            ticket.attach_file = request.FILES['attach_file']

        ticket.subject = request.POST['subject']
        ticket.description = request.POST['description']
        ticket.save()

        return redirect('user_mytickets')
    else:
        print("di post")
    return render(request,'user-mytickets.html')

def user_delete_ticket(request):
    if request.method == 'POST':
        ticket = tickets.objects.get(id=request.POST["id"])
        ticket.delete()
        return redirect("user_mytickets")
        
    return render(request,'user-mytickets.html')

def user_delete_reply(request):
    if request.method == 'POST':
        reply = replies.objects.get(id=request.POST["id"])
        pk = reply.ticket_id
        reply.delete()
        return redirect('user_view_myticket', pk=pk )

    return render(request,'user-view-mytickets.html')

def user_add_reply(request):
    if request.method == 'POST':
        reply=replies()
        reply.ticket = tickets.objects.get(id=request.POST['ticket'])
        pk = reply.ticket_id
        reply.message = request.POST['reply_msg']

        if request.FILES.get('attach_file', False):
            reply.attach_file = request.FILES['attach_file']

        reply.save()
        print("reply created")
        return redirect('user_view_myticket', pk=pk)

    return render(request,'user-view-mytickets.html')


    















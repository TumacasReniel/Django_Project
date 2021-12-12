from django .contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render,redirect

from django.contrib import messages
from django.contrib.auth import get_user_model

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from ST_System.models import *
from .models import agent_od

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_activation_token


# Create your views here.
from .forms import *

def signup(request):
    User = get_user_model()
    dep = departments.objects.all()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        status= request.POST['status']
        department =  departments.objects.get(department_name=request.POST['department'])
        dep = department.id

        department =  departments.objects.get(id=dep)


        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'Username already taken')
                return redirect('login')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,'Email already taken')
                return redirect('login')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name,status=status,department =department)
                # user can't login until link confirmed
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'

                # load a template like get_template() 
                # and calls its render() method immediately.
                template = render_to_string('acc_active_email.html',{'name':first_name,'username':username,'password':password1,'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': default_token_generator.make_token(user),
                })

                email = EmailMessage(
                    mail_subject,  
                    template,
                    settings.EMAIL_HOST_USER,
                    [email],
                )

                email.fail_silently=False
                email.send()

                messages.success(request,'Please check your email and confirm your email address to complete your account registration')
               
                return redirect('signup')
        
        else:
            messages.warning(request,'Password not matching')
        return redirect('signup')

    context = {
        "dep":dep
    }
    return render(request,'signup.html',context)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

     # checking if the user exists, if the token is valid.
    if user is not None and default_token_generator.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def User_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            if user.status == "ADMINISTRATOR" or user.is_superuser:
                auth.login(request,user)
                return redirect('admin_dashboard')
            elif user.status == "SUPPORT AGENT":
                auth.login(request,user)
                return redirect('agent_dashboard_one')
            elif user.status == "USER":
                auth.login(request,user)
                return redirect('user_dashboard')
            else:
                messages.warning(request,'account disabled')
                return redirect('login')
        else:
            messages.warning(request,'Invalid username or password')
            return redirect('login')
    else:
        return render(request,'login.html')

def User_logout(request):
    auth.logout(request)
    return render(request,'index.html')

    

def add_admin(request):
    if request.method == 'POST':
        User = get_user_model()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        status= request.POST['status']
        department = departments.objects.get(id=request.POST['department'])

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'Username already taken')
                return redirect('login')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,'Email already taken')
                return redirect('login')
            else:
                user = User.objects.create_agent(username=username,password=password1,email=email,first_name=first_name,last_name=last_name,status=status,department=department)
                user.save()

                
                print('admin account created')
                return redirect('admin_users')
        else:
            messages.warning(request,'Password not matching')
        return redirect('admin_users')
    return render(request,'admin-users.html')

def add_user(request):
    if request.method == 'POST':
        User = get_user_model()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        status= request.POST['status']
        department = departments.objects.get(id=request.POST['department'])

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'Username already taken')
                return redirect('login')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,'Email already taken')
                return redirect('login')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name,status=status,department=department)
                user.save()
                
                print('user account created')
                return redirect('admin_users')
        else:
            messages.warning(request,'Password not matching')
        return redirect('admin_users')
    return render(request,'admin-users.html')

def add_agent(request):
    if request.method == 'POST':
        User = get_user_model()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        status= request.POST['status']

        department = departments.objects.get(id=request.POST['department'])
        category = categories.objects.get(id=request.POST['category'])
        level = request.POST['level']


        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'Username already taken')
                return redirect('login')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,'Email already taken')
                return redirect('login')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name,status=status,department=department)
                user.save()

                agent= agent_od()
                agent.user= User.objects.get(id=user.id)
                agent.category=category
                agent.level=level

                agent.save()

                print('admin account created')
                return redirect('admin_users')
        else:
            messages.warning(request,'Password not matching')
        return redirect('admin_users')
    return render(request,'admin-users.html')

def admin_delete_account(request):
    User = get_user_model()
    if request.method == 'POST':
        user = User.objects.get(id=request.POST['id'])
        user.delete()
        return redirect('admin_users')

    return render(request, 'admin-users.html')

def admin_update_account(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST['id'])

        if user.status == "USER":
            form = userForm(request.POST, instance=user)
        elif user.status == "SUPPORT AGENT":
            form = agentForm(request.POST, instance=user)
        elif user.status == "ADMINISTRATOR":
            form = adminForm(request.POST, instance=user)
 
        if form.is_valid():
            form.save()
            return redirect('admin_users')
        else:
            print("di valid")
            return HttpResponse(form)
    
    return render(request, 'admin-users.html')

def admin_update_agent_assigned(request):
    if request.method == 'POST':
        od = agent_od.objects.get(user_id=request.POST['id'])

        form = assForm(request.POST, instance=od)

        if form.is_valid():
            form.save()
            return redirect('admin_users')
        else:
            print("di valid")
            return HttpResponse(form)
    
    return render(request, 'admin-users.html')

def admin_change_profile(request):
    if request.method == 'POST':
        User = get_user_model()
        user= User.objects.get(id=request.POST['id'])
        form = profileForm(request.POST,request.FILES,instance=user)

        if form.is_valid():
            form.save()
            return redirect('admin_profile')

    return render(request, 'admin-profile.html')

def agent_change_profile(request):
    if request.method == 'POST':
        User = get_user_model()
        user= User.objects.get(id=request.POST['id'])
        form = profileForm(request.POST,request.FILES,instance=user)

        if form.is_valid():
            form.save()
            return redirect('agent_profile')

    return render(request, 'agent-profile.html')

def user_change_profile(request):
    if request.method == 'POST':
        User = get_user_model()
        user= User.objects.get(id=request.POST['id'])
        form = profileForm(request.POST,request.FILES,instance=user)

        if form.is_valid():
            form.save()
            return redirect('user_profile')

    return render(request, 'user-profile.html')
        



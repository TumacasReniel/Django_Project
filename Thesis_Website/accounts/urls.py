from django.urls import path

from . import views


# urlpatterns = [
#     path("signup1",views.signup1, name='signup1'),
# ] 

urlpatterns = [
    path("signup",views.signup, name='signup'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'), 
    path("login",views.User_login, name='login'),
    path("logout",views.User_logout, name='logout'),
    path("add_admin",views.add_admin, name='add_admin'),
    path("admin_delete_account",views.admin_delete_account, name='admin_delete_account'),
    path("admin_update_account",views.admin_update_account, name='admin_update_account'),
    path("admin_update_agent_assigned",views.admin_update_agent_assigned, name='admin_update_agent_assigned'),
    path("add_user",views.add_user, name='add_user'),
    path("add_agent",views.add_agent, name='add_agent'),
    path("admin_change_profile",views.admin_change_profile, name='admin_change_profile'),
    path("agent_change_profile",views.agent_change_profile, name='agent_change_profile'),
    path("user_change_profile",views.user_change_profile, name='user_change_profile'),
] 


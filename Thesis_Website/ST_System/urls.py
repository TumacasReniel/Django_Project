from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    

    #admin

    path("admin_dashboard",views.admin_dashboard, name='admin_dashboard'),
    path("admin_tickets",views.admin_tickets, name='admin_tickets'),
    path("admin_ticket_statuses",views.admin_ticket_statuses, name='admin_ticket_statuses'),
    path("admin_departments",views.admin_departments, name='admin_departments'),
    path("admin_users",views.admin_users, name='admin_users'),
    path("admin_categories",views.admin_categories, name='admin_categories'),
    # path("admin_assignees",views.admin_assignees, name='admin_assignees'),
    path("admin_priorities",views.admin_priorities, name='admin_priorities'), 
    path("admin_profile",views.admin_profile, name='admin_profile'), 

    #add ticket status
    path("add_ticket_status",views.add_ticket_status, name='add_ticket_status'),

    #delete ticket status
    path("admin_delete_ticket_status",views.admin_delete_ticket_status, name='admin_delete_ticket_status'),

    #update ticket status
    path("admin_update_ticket_status",views.admin_update_ticket_status, name='admin_update_ticket_status'),

    #add department
    path("add_department",views.add_department, name='add_department'),

    #delete department
    path("admin_delete_department",views.admin_delete_department, name='admin_delete_department'),

    #update department
    path("admin_update_department",views.admin_update_department, name='admin_update_department'),


    #add category
    path("add_category",views.add_category, name='add_category'),

    #delete category
    path("admin_delete_category",views.admin_delete_category, name='admin_delete_category'),

    #update category
    path("admin_update_category",views.admin_update_category, name='admin_update_category'),


    #add sub-category
    path("add_sub_category",views.add_sub_category, name='add_sub_category'),
    
    #delete subcategory
    path("admin_delete_sub_category",views.admin_delete_sub_category, name='admin_delete_sub_category'),

    #update subcategory
    path("admin_update_sub_category",views.admin_update_sub_category, name='admin_update_sub_category'),

    #assign agent
    # path("assign_agent",views.assign_agent, name='assign_agent'),

    #view more agent 
    path("admin_agent_view_more/<int:pk>/",views.admin_agent_view_more, name='admin_agent_view_more'),

    #view more admin
    path("admin_admin_view_more/<int:pk>/",views.admin_admin_view_more, name='admin_admin_view_more'),

    #agent load categories
    path("admin_user_view_more/<int:pk>/",views.admin_user_view_more, name='admin_user_view_more'),

    #admin filter ticket
    #path("admin_filter_ticket",views.admin_filter_ticket, name='admin_filter_ticket'),

    

    #agent
    path("agent_dashboard_one",views.agent_dashboard_one, name='agent_dashboard_one'),
    path("agent_dashboard_two",views.agent_dashboard_two, name='agent_dashboard_two'),
    path("agent_profile",views.agent_profile, name='agent_profile'),
    path("agent_mytickets",views.agent_mytickets, name='agent_mytickets'),
    path("agent_accepted_tickets",views.agent_accepted_tickets, name='agent_accepted_tickets'),
    path("view_ticket/<int:pk>/",views.view_ticket, name='view_ticket'),
    path("agent_view_accepted_ticket/<int:pk>/",views.agent_view_accepted_ticket, name='agent_view_accepted_ticket'),
    path("agent_add_reply_on_accepted_ticket",views.agent_add_reply_on_accepted_ticket, name='agent_add_reply_on_accepted_ticket'),

    path("agent_delete_ticket",views.agent_delete_ticket, name='agent_delete_ticket'),
    # path("agent_view_ticket_modal",views.agent_view_ticket_modal, name='agent_view_ticket_modal'),
    path("create_ticket",views.create_ticket, name='create_ticket'),
    path("accept_ticket",views.accept_ticket, name='accept_ticket'),
    path("add_reply",views.add_reply, name='add_reply'),
    path("delete_reply",views.delete_reply, name='delete_reply'),

    path("agent_tag_tickets",views.agent_tag_tickets, name='agent_tag_tickets'),
    path("agent_invite_agent",views.agent_invite_agent, name='agent_invite_agent'),

    path('ajax_load_categories', views.ajax_load_categories, name='ajax_load_categories'), # AJAX
    path('ajax_load_sub_categories', views.ajax_load_sub_categories, name='ajax_load_sub_categories'), # AJAX
    

    #end-user

    path("user_mytickets",views.user_mytickets, name='user_mytickets'),
    path("user_profile",views.user_profile, name='user_profile'),

    path("user_view_ticket/<int:pk>/",views.user_view_ticket, name='user_view_ticket'),

    path("user_dashboard",views.user_dashboard, name='user_dashboard'),
    path("user_view_myticket/<int:pk>/",views.user_view_myticket, name='user_view_myticket'),path("user_create_ticket",views.user_create_ticket, name='user_create_ticket'),
    path("user_delete_ticket",views.user_delete_ticket, name='user_delete_ticket'),
    path("user_add_reply",views.user_add_reply, name='user_add_reply'),
    path("user_delete_reply",views.user_delete_reply, name='user_delete_reply'),

    
    
] 


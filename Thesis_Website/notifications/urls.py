from django.urls import path

from . import views


urlpatterns = [
    path("user_notifications",views.user_notifications, name='user_notifications'),
    path("user_delete_notification",views.user_delete_notification, name='user_delete_notification'),
    path("user_see_notification/<int:pk>/",views.user_see_notification, name='user_see_notification'),
    path("agent_notifications",views.agent_notifications, name='agent_notifications'),
    path("agent_see_notification/<int:pk>/",views.agent_see_notification, name='agent_see_notification'),
    path("agent_delete_notification",views.agent_delete_notification, name='agent_delete_notification'),
] 


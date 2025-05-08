from django.urls import path
from . import views

app_name = 'user_messages'

urlpatterns = [
    # Regular user messaging URLs
    path('inbox/', views.user_inbox, name='inbox'),
    path('compose/', views.compose_message, name='compose'),
    path('detail/<int:message_id>/', views.message_detail, name='detail'),
    path('sent/', views.sent_messages, name='sent'),
    path('mark_important/<int:message_id>/', views.mark_important, name='mark_important'),
    path('important/', views.important_messages, name='important'),
    path('delete/<int:message_id>/', views.delete_message, name='delete'),
    path('contact-support/', views.contact_support, name='contact_support'),


    # Admin-specific messaging URLs
    path('admin/inbox/', views.admin_inbox, name='admin_inbox'),
    path('admin/compose/<int:message_id>/', views.admin_compose_message, name='admin_compose_reply'),
    path('admin/compose/', views.admin_compose_message, name='admin_compose'),
    path('admin/delete/<int:message_id>/', views.admin_delete_message, name='admin_delete_message'),
    path('admin/detail/<int:message_id>/', views.message_detail, name='admin_message_detail'),
    path('history/<int:user_id>/', views.conversation_history, name='conversation_history'),
]

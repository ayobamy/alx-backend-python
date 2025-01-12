from django.urls import path
from . import views

urlpatterns = [
    path('user/delete/', views.delete_user, name='delete_user'),
    path('messages/<int:message_id>/', views.handle_message, name='handle_message'),
    path('messages/<int:message_id>/history/', views.message_history, name='message_history'),
    path('messages/<int:message_id>/thread/', views.get_threaded_conversation, name='threaded_conversation'),
    path('messages/unread/', views.unread_messages, name='unread_messages'),
]

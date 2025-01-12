from django.urls import path
from . import views

urlpatterns = [
    path('user/delete/', views.delete_user, name='delete_user'),
    path('conversation/<int:other_user_id>/', views.conversation_messages, name='conversation'),
    path('message/<int:message_id>/thread/', views.get_threaded_conversation, name='threaded_conversation'),
    path('messages/unread/', views.unread_messages, name='unread_messages'),
    path('message/<int:message_id>/history/', views.message_history, name='message_history'),
]

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import Message, MessageHistory

@login_required
@require_http_methods(["GET", "POST"])
def delete_user(request):
    """
    View to delete a user account and clean up related data.
    """
    if request.method == 'GET':
        return render(request, 'messaging/delete_account.html')
    
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('login')

@cache_page(60)
@login_required
def conversation_messages(request, other_user_id):
    """
    Retrieve conversation between current user and another user.
    """
    other_user = get_object_or_404(User, id=other_user_id)
    
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).prefetch_related(
        Prefetch('replies'),
        'history'
    ).select_related('sender', 'receiver')
    
    Message.objects.filter(receiver=request.user, read=False).update(read=True)
    
    if request.headers.get('Accept') == 'application/json':
        data = [{
            'id': msg.id,
            'content': msg.content,
            'sender': msg.sender.username,
            'receiver': msg.receiver.username,
            'timestamp': msg.timestamp.isoformat(),
            'edited': msg.edited,
            'read': msg.read
        } for msg in messages]
        return JsonResponse(data, safe=False)
    
    return render(request, 'messaging/conversation.html', {
        'messages': messages,
        'other_user': other_user
    })

@login_required
def get_threaded_conversation(request, message_id):
    """
    Fetch a message and all its replies recursively.
    """
    def fetch_replies(message):
        replies = message.replies.prefetch_related(
            'sender', 'receiver'
        ).select_related('parent_message', 'sender', 'receiver')
        
        return [{
            'id': reply.id,
            'content': reply.content,
            'sender': reply.sender.username,
            'receiver': reply.receiver.username,
            'timestamp': reply.timestamp.isoformat(),
            'edited': reply.edited,
            'read': reply.read,
            'replies': fetch_replies(reply)
        } for reply in replies]

    # Get the root message and verify access
    root_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver', 'parent_message'),
        id=message_id
    )
    
    if request.user not in [root_message.sender, root_message.receiver]:
        raise PermissionDenied("You don't have permission to view this conversation")
    
    conversation = {
        'id': root_message.id,
        'content': root_message.content,
        'sender': root_message.sender.username,
        'receiver': root_message.receiver.username,
        'timestamp': root_message.timestamp.isoformat(),
        'edited': root_message.edited,
        'read': root_message.read,
        'replies': fetch_replies(root_message)
    }
    
    return JsonResponse(conversation)

@cache_page(60)
@login_required
def unread_messages(request):
    """
    Retrieve all unread messages for the logged-in user.
    """
    messages = Message.objects.get_unread_messages(request.user)
    
    if request.headers.get('Accept') == 'application/json':
        data = [{
            'id': msg.id,
            'sender': msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]
        return JsonResponse(data, safe=False)
    
    return render(request, 'messaging/unread.html', {'messages': messages})

@login_required
def message_history(request, message_id):
    """
    Retrieve edit history for a specific message.
    """
    message = get_object_or_404(Message, id=message_id)
    
    if request.user not in [message.sender, message.receiver]:
        raise PermissionDenied("You don't have permission to view this message history")
    
    history = message.history.all().order_by('-edited_at')
    
    if request.headers.get('Accept') == 'application/json':
        data = {
            'message': {
                'id': message.id,
                'current_content': message.content,
                'sender': message.sender.username,
                'receiver': message.receiver.username
            },
            'history': [{
                'old_content': entry.old_content,
                'edited_at': entry.edited_at.isoformat()
            } for entry in history]
        }
        return JsonResponse(data)
    
    return render(request, 'messaging/history.html', {
        'message': message,
        'history': history
    })

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, Prefetch
from .models import Message, MessageHistory
import json

@login_required
@require_http_methods(["DELETE"])
def delete_user(request):
    """
    Delete user account and return success response
    """
    user = request.user
    Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).delete()
    user.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'User account deleted successfully'
    })

@login_required
@require_http_methods(["GET", "PUT"])
def handle_message(request, message_id):
    """
    Handle message operations (get/edit)
    """
    message = get_object_or_404(
        Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).select_related(
            'sender',
            'receiver',
            'last_edited_by'
        ).prefetch_related(
            'replies'
        ),
        id=message_id
    )
    
    if request.method == "GET":
        return JsonResponse({
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'timestamp': message.timestamp.isoformat(),
            'edited': message.edited,
            'last_edited_by': message.last_edited_by.username if message.last_edited_by else None,
            'last_edited_at': message.last_edited_at.isoformat() if message.last_edited_at else None,
            'reply_count': message.replies.count()
        })
    
    if request.method == "PUT":
        if message.sender != request.user:
            raise PermissionDenied("You can only edit your own messages")
            
        try:
            data = json.loads(request.body)
            new_content = data.get('content')
            
            if not new_content:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Content is required'
                }, status=400)
                
            if new_content != message.content:
                message.content = new_content
                message.last_edited_by = request.user
                message.last_edited_at = timezone.now()
                message.save()
                
            return JsonResponse({
                'status': 'success',
                'message': 'Message updated successfully',
                'content': message.content,
                'last_edited_at': message.last_edited_at.isoformat()
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)

@login_required
def message_history(request, message_id):
    """
    Get message edit history
    """
    message = get_object_or_404(
        Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).select_related(
            'sender',
            'receiver',
            'last_edited_by'
        ),
        id=message_id
    )
    
    history = message.history.select_related('edited_by').order_by('-edited_at')
    
    return JsonResponse({
        'message': {
            'id': message.id,
            'current_content': message.content,
            'last_edited_by': message.last_edited_by.username if message.last_edited_by else None,
            'last_edited_at': message.last_edited_at.isoformat() if message.last_edited_at else None
        },
        'history': [{
            'old_content': entry.old_content,
            'edited_by': entry.edited_by.username if entry.edited_by else None,
            'edited_at': entry.edited_at.isoformat()
        } for entry in history]
    })

@cache_page(60)
@login_required
def get_threaded_conversation(request, message_id):
    """
    Get threaded conversation using recursive query
    """
    def fetch_replies(message):
        replies = Message.objects.filter(
            parent_message=message
        ).select_related(
            'sender',
            'receiver',
            'parent_message',
            'last_edited_by'
        ).prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related(
                'sender', 'receiver', 'last_edited_by'
            ))
        )
        
        return [{
            'id': reply.id,
            'content': reply.content,
            'sender': reply.sender.username,
            'receiver': reply.receiver.username,
            'timestamp': reply.timestamp.isoformat(),
            'edited': reply.edited,
            'last_edited_by': reply.last_edited_by.username if reply.last_edited_by else None,
            'last_edited_at': reply.last_edited_at.isoformat() if reply.last_edited_at else None,
            'replies': fetch_replies(reply)
        } for reply in replies]

    root_message = get_object_or_404(
        Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).select_related(
            'sender',
            'receiver',
            'parent_message',
            'last_edited_by'
        ),
        id=message_id
    )
    
    return JsonResponse({
        'id': root_message.id,
        'content': root_message.content,
        'sender': root_message.sender.username,
        'receiver': root_message.receiver.username,
        'timestamp': root_message.timestamp.isoformat(),
        'edited': root_message.edited,
        'last_edited_by': root_message.last_edited_by.username if root_message.last_edited_by else None,
        'last_edited_at': root_message.last_edited_at.isoformat() if root_message.last_edited_at else None,
        'replies': fetch_replies(root_message)
    })

@cache_page(60)
@login_required
def unread_messages(request):
    """
    Get unread messages with optimized queries
    """
    messages = Message.unread.unread_for_user(request.user).only(
        'id', 
        'content',
        'timestamp',
        'edited',
        'last_edited_at',
        'sender__username',
        'last_edited_by__username'
    ).select_related(
        'sender',
        'last_edited_by'
    ).prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related(
            'sender', 'receiver'
        ))
    )
    
    return JsonResponse({
        'unread_messages': [{
            'id': msg.id,
            'sender': msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat(),
            'edited': msg.edited,
            'last_edited_by': msg.last_edited_by.username if msg.last_edited_by else None,
            'last_edited_at': msg.last_edited_at.isoformat() if msg.last_edited_at else None,
            'reply_count': msg.replies.count()
        } for msg in messages]
    })

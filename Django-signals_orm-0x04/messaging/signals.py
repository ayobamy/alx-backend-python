from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Create notification when a new message is created
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Log message edits in MessageHistory
    """
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                instance.edited = True
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Clean up user-related data after user deletion
    """
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()

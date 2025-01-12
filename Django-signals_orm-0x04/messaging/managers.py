from django.db import models

class UnreadMessagesManager(models.Manager):
    def get_unread_messages(self, user):
        """
        Get all unread messages for a user
        """
        return self.filter(receiver=user, read=False).only(
            'sender', 'content', 'timestamp', 'read'
        ).select_related('sender')

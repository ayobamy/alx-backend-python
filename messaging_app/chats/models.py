import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User model
    """
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        unique=True,
        db_index=True
    )

    password = models.CharField(
        max_length=128,
        help_text="User's hashed password"
    )
    
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True
    )
    
    class Role(models.TextChoices):
        GUEST = 'guest', 'Guest User'
        HOST = 'host', 'Host User'
        ADMIN = 'admin', 'Admin User'
  
    role = models.CharField(
        max_length=10, 
        choices=Role.choices, 
        default=Role.GUEST,
        null=False
    )
    
    email = models.EmailField(
        unique=True, 
        null=False, 
        blank=False
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

class Conversation(models.Model):
    """
    Conversation model
    """
    conversation_id  = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        unique=True,
        db_index=True
    )
    
    participants = models.ManyToManyField(
        User, 
        related_name='conversations',
        blank=True
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        participant_names = ", ".join([
            user.first_name for user in self.participants.all()
        ])
        return f"Conversation {self.conversation_id}"
    
    class Meta:
        verbose_name_plural = 'Conversations'
        ordering = ['-created_at']

class Message(models.Model):
    """
    Msg model
    """
    message_id  = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        unique=True,
        db_index=True
    )
    
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    message_body = models.TextField(
        null=False, 
        blank=False
    )
    
    sent_at = models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        return f"Message {self.message_id} in conversation {self.conversation.conversation_id}"
    
    class Meta:
        verbose_name_plural = 'Messages'
        ordering = ['-sent_at']

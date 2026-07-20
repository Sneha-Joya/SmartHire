from django.db import models
from accounts.models import User
from jobs.models import Job


class Conversation(models.Model):
    """Represents a conversation between two users"""
    participants = models.ManyToManyField(User, related_name='conversations')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='conversations', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        participants_list = list(self.participants.all())
        if len(participants_list) == 2:
            return f"Conversation: {participants_list[0].username} & {participants_list[1].username}"
        return f"Conversation: {self.id}"

    def get_other_participant(self, user):
        """Get the other participant in the conversation"""
        participants = list(self.participants.exclude(id=user.id))
        return participants[0] if participants else None


class Message(models.Model):
    """Represents a message in a conversation"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} in {self.conversation}"



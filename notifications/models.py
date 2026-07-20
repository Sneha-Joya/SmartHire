from django.db import models
from accounts.models import User
from jobs.models import Job, Application


class Notification(models.Model):
    """In-app notification system"""
    NOTIFICATION_TYPES = [
        ('application_received', 'Application Received'),
        ('application_accepted', 'Application Accepted'),
        ('application_rejected', 'Application Rejected'),
        ('job_posted', 'Job Posted'),
        ('message_received', 'Message Received'),
        ('job_completed', 'Job Completed'),
        ('review_received', 'Review Received'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    related_application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"



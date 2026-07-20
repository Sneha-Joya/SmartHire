from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from jobs.models import Job, Application


class Review(models.Model):
    """Review and rating system"""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['job', 'reviewer', 'reviewed_user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer.username} rated {self.reviewed_user.username} {self.rating} stars"



from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    required_skills = models.CharField(max_length=500, help_text="Comma-separated list of required skills")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.client.username}"

    def get_required_skills_list(self):
        """Return required skills as a list"""
        if self.required_skills:
            return [skill.strip() for skill in self.required_skills.split(',')]
        return []

    class Meta:
        ordering = ['-created_at']


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    proposal = models.TextField()
    proposed_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)]
    )
    estimated_hours = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    hired_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.freelancer.username} - {self.job.title}"

    class Meta:
        unique_together = ['job', 'freelancer']
        ordering = ['-created_at']


class Project(models.Model):
    """Represents an active project after hiring"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='project')
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='project')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_projects')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Project: {self.job.title} - {self.freelancer.username}"

    class Meta:
        ordering = ['-created_at']


class ProjectUpdate(models.Model):
    """Status updates from freelancer on project progress"""
    UPDATE_STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('milestone_reached', 'Milestone Reached'),
        ('review_needed', 'Review Needed'),
        ('revision_requested', 'Revision Requested'),
        ('ready_for_review', 'Ready for Review'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_updates')
    status = models.CharField(max_length=30, choices=UPDATE_STATUS_CHOICES, default='in_progress')
    title = models.CharField(max_length=200)
    description = models.TextField()
    attachment = models.FileField(upload_to='project_updates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Update: {self.title} - {self.project.job.title}"


class ProjectFeedback(models.Model):
    """Client feedback on project updates"""
    FEEDBACK_TYPE_CHOICES = [
        ('approval', 'Approval'),
        ('revision', 'Revision Request'),
        ('question', 'Question'),
        ('compliment', 'Compliment'),
    ]
    
    project_update = models.ForeignKey(ProjectUpdate, on_delete=models.CASCADE, related_name='feedbacks')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_feedbacks')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES, default='approval')
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback on {self.project_update.title} by {self.client.username}"


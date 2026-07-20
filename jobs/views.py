from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Job, Application, Category, Project, ProjectUpdate, ProjectFeedback
from .forms import JobForm, ApplicationForm, ProjectUpdateForm, ProjectFeedbackForm
from notifications.models import Notification


def home(request):
    """Home page - landing page for non-authenticated, role-based for authenticated"""
    if not request.user.is_authenticated:
        # Show landing page for non-authenticated users
        return render(request, 'jobs/landing.html')
    
    # Role-based content for authenticated users
    jobs = Job.objects.filter(status='open').order_by('-created_at')
    categories = Category.objects.all()[:8]
    
    # Search functionality
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    budget_min = request.GET.get('budget_min', '')
    budget_max = request.GET.get('budget_max', '')
    
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    if category_filter:
        jobs = jobs.filter(category_id=category_filter)
    
    if budget_min:
        try:
            jobs = jobs.filter(budget__gte=float(budget_min))
        except ValueError:
            pass
    
    if budget_max:
        try:
            jobs = jobs.filter(budget__lte=float(budget_max))
        except ValueError:
            pass
    
    # Pagination
    paginator = Paginator(jobs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'jobs': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
        'budget_min': budget_min,
        'budget_max': budget_max,
    }
    return render(request, 'jobs/home.html', context)


@login_required
def job_detail(request, job_id):
    """View job details - requires login"""
    job = get_object_or_404(Job, id=job_id)
    has_applied = False
    application = None
    
    if request.user.user_type == 'freelancer':
        application = Application.objects.filter(job=job, freelancer=request.user).first()
        has_applied = application is not None
    
    context = {
        'job': job,
        'has_applied': has_applied,
        'application': application,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def post_job(request):
    """Allow clients to post a new job"""
    if request.user.user_type != 'client':
        messages.error(request, 'Only clients can post jobs.')
        return redirect('jobs:home')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs:job_detail', job_id=job.id)
    else:
        form = JobForm()
    
    return render(request, 'jobs/post_job.html', {'form': form})


@login_required
def apply_job(request, job_id):
    """Allow freelancers to apply for a job"""
    if request.user.user_type != 'freelancer':
        messages.error(request, 'Only freelancers can apply for jobs.')
        return redirect('jobs:home')
    
    job = get_object_or_404(Job, id=job_id)
    
    # Check if already applied
    if Application.objects.filter(job=job, freelancer=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', job_id=job.id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.freelancer = request.user
            application.save()
            
            # Create notification for client
            Notification.objects.create(
                user=job.client,
                notification_type='application_received',
                title='New Application',
                message=f"{request.user.username} applied for your job: {job.title}",
                related_job=job,
                related_application=application
            )
            
            messages.success(request, 'Application submitted successfully!')
            return redirect('jobs:job_detail', job_id=job.id)
    else:
        form = ApplicationForm()
    
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


@login_required
def my_jobs(request):
    """Show jobs posted by the current client"""
    if request.user.user_type != 'client':
        messages.error(request, 'Only clients can view their posted jobs.')
        return redirect('jobs:home')
    
    jobs = Job.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})


@login_required
def my_applications(request):
    """Show applications made by the current freelancer"""
    if request.user.user_type != 'freelancer':
        messages.error(request, 'Only freelancers can view their applications.')
        return redirect('jobs:home')
    
    applications = Application.objects.filter(freelancer=request.user).order_by('-created_at')
    return render(request, 'jobs/my_applications.html', {'applications': applications})


@login_required
def manage_applications(request, job_id):
    """Allow clients to view and manage applications for their job"""
    job = get_object_or_404(Job, id=job_id)
    
    if job.client != request.user:
        messages.error(request, 'You can only manage applications for your own jobs.')
        return redirect('jobs:home')
    
    applications = Application.objects.filter(job=job).order_by('-created_at')
    return render(request, 'jobs/manage_applications.html', {'job': job, 'applications': applications})


@login_required
def accept_application(request, application_id):
    """Allow clients to accept an application and hire freelancer"""
    application = get_object_or_404(Application, id=application_id)
    
    if application.job.client != request.user:
        messages.error(request, 'You can only accept applications for your own jobs.')
        return redirect('jobs:home')
    
    if application.status != 'pending':
        messages.warning(request, 'This application has already been processed.')
        return redirect('jobs:manage_applications', job_id=application.job.id)
    
    # Check if job already has a project
    if Project.objects.filter(job=application.job).exists():
        messages.error(request, 'This job already has a freelancer assigned.')
        return redirect('jobs:manage_applications', job_id=application.job.id)
    
    application.status = 'hired'
    application.hired_at = timezone.now()
    application.save()
    
    # Create project
    project = Project.objects.create(
        job=application.job,
        application=application,
        client=request.user,
        freelancer=application.freelancer,
        status='active'
    )
    
    # Update job status
    application.job.status = 'in_progress'
    application.job.save()
    
    # Reject other applications
    Application.objects.filter(
        job=application.job,
        status='pending'
    ).exclude(id=application.id).update(status='rejected')
    
    # Create notifications
    Notification.objects.create(
        user=application.freelancer,
        notification_type='application_accepted',
        title='Application Accepted!',
        message=f"Congratulations! Your application for '{application.job.title}' has been accepted.",
        related_job=application.job,
        related_application=application
    )
    
    # Notify rejected applicants
    rejected_applications = Application.objects.filter(
        job=application.job,
        status='rejected'
    )
    for rejected_app in rejected_applications:
        Notification.objects.create(
            user=rejected_app.freelancer,
            notification_type='application_rejected',
            title='Application Update',
            message=f"Your application for '{application.job.title}' was not selected.",
            related_job=application.job,
            related_application=rejected_app
        )
    
    messages.success(request, f'Freelancer hired! {application.freelancer.username} is now working on this project.')
    return redirect('jobs:manage_applications', job_id=application.job.id)


@login_required
def reject_application(request, application_id):
    """Allow clients to reject an application"""
    application = get_object_or_404(Application, id=application_id)
    
    if application.job.client != request.user:
        messages.error(request, 'You can only reject applications for your own jobs.')
        return redirect('jobs:home')
    
    if application.status != 'pending':
        messages.warning(request, 'This application has already been processed.')
        return redirect('jobs:manage_applications', job_id=application.job.id)
    
    application.status = 'rejected'
    application.save()
    
    # Create notification
    Notification.objects.create(
        user=application.freelancer,
        notification_type='application_rejected',
        title='Application Update',
        message=f"Your application for '{application.job.title}' was rejected.",
        related_job=application.job,
        related_application=application
    )
    
    messages.success(request, 'Application rejected.')
    return redirect('jobs:manage_applications', job_id=application.job.id)


@login_required
def my_projects(request):
    """Show active projects for the current user"""
    if request.user.user_type == 'client':
        projects = Project.objects.filter(client=request.user).order_by('-created_at')
    elif request.user.user_type == 'freelancer':
        projects = Project.objects.filter(freelancer=request.user).order_by('-created_at')
    else:
        messages.error(request, 'Only clients and freelancers can view projects.')
        return redirect('jobs:home')
    
    # Add review status for each project
    from reviews.models import Review
    projects_with_reviews = []
    for project in projects:
        has_review = False
        if project.status == 'completed' and request.user.user_type == 'client':
            has_review = Review.objects.filter(job=project.job, reviewer=request.user).exists()
        projects_with_reviews.append({
            'project': project,
            'has_review': has_review,
        })
    
    return render(request, 'jobs/my_projects.html', {'projects_data': projects_with_reviews})


@login_required
def project_detail(request, project_id):
    """View project details"""
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user is part of this project
    if project.client != request.user and project.freelancer != request.user:
        messages.error(request, 'You do not have access to this project.')
        return redirect('jobs:home')
    
    # Get all updates and their feedbacks
    updates = ProjectUpdate.objects.filter(project=project).order_by('-created_at')
    
    # Check if client has already reviewed
    has_review = False
    if project.status == 'completed' and request.user.user_type == 'client' and project.client == request.user:
        from reviews.models import Review
        has_review = Review.objects.filter(job=project.job, reviewer=request.user).exists()
    
    context = {
        'project': project,
        'updates': updates,
        'has_review': has_review,
    }
    return render(request, 'jobs/project_detail.html', context)


@login_required
def complete_project(request, project_id):
    """Mark project as completed"""
    project = get_object_or_404(Project, id=project_id)
    
    if project.client != request.user:
        messages.error(request, 'Only the client can mark a project as completed.')
        return redirect('jobs:project_detail', project_id=project_id)
    
    if project.status == 'completed':
        messages.warning(request, 'This project is already completed.')
        return redirect('jobs:project_detail', project_id=project_id)
    
    project.status = 'completed'
    project.completed_at = timezone.now()
    project.save()
    
    # Update job status
    project.job.status = 'completed'
    project.job.save()
    
    # Update freelancer profile
    if project.freelancer.freelancer_profile:
        profile = project.freelancer.freelancer_profile
        profile.total_projects += 1
        profile.save()
    
    # Create notifications
    Notification.objects.create(
        user=project.freelancer,
        notification_type='job_completed',
        title='Project Completed',
        message=f"The project '{project.job.title}' has been marked as completed.",
        related_job=project.job
    )
    
    messages.success(request, 'Project marked as completed! You can now leave a review.')
    return redirect('jobs:project_detail', project_id=project_id)


@login_required
def create_project_update(request, project_id):
    """Freelancer creates a project status update"""
    project = get_object_or_404(Project, id=project_id)
    
    if project.freelancer != request.user:
        messages.error(request, 'Only the freelancer assigned to this project can create updates.')
        return redirect('jobs:project_detail', project_id=project_id)
    
    if project.status != 'active':
        messages.error(request, 'You can only create updates for active projects.')
        return redirect('jobs:project_detail', project_id=project_id)
    
    if request.method == 'POST':
        form = ProjectUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.project = project
            update.freelancer = request.user
            update.save()
            
            # Create notification for client
            Notification.objects.create(
                user=project.client,
                notification_type='job_posted',  # Reusing this type for update notifications
                title='Project Update',
                message=f"{request.user.username} posted an update on '{project.job.title}': {update.title}",
                related_job=project.job
            )
            
            messages.success(request, 'Project update posted successfully!')
            return redirect('jobs:project_detail', project_id=project_id)
    else:
        form = ProjectUpdateForm()
    
    return render(request, 'jobs/create_project_update.html', {
        'form': form,
        'project': project,
    })


@login_required
def add_project_feedback(request, update_id):
    """Client adds feedback on a project update"""
    update = get_object_or_404(ProjectUpdate, id=update_id)
    project = update.project
    
    if project.client != request.user:
        messages.error(request, 'Only the client can provide feedback on project updates.')
        return redirect('jobs:project_detail', project_id=project.id)
    
    if request.method == 'POST':
        form = ProjectFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.project_update = update
            feedback.client = request.user
            feedback.save()
            
            # Create notification for freelancer
            Notification.objects.create(
                user=project.freelancer,
                notification_type='application_received',  # Reusing this type
                title='Project Feedback',
                message=f"{request.user.username} provided feedback on your update: '{update.title}'",
                related_job=project.job
            )
            
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('jobs:project_detail', project_id=project.id)
    else:
        form = ProjectFeedbackForm()
    
    return render(request, 'jobs/add_project_feedback.html', {
        'form': form,
        'update': update,
        'project': project,
    })


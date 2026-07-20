from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job, Project
from .models import Review
from .forms import ReviewForm
from notifications.models import Notification


@login_required
def create_review(request, job_id):
    """Create a review for a completed job - Only clients can review freelancers"""
    job = get_object_or_404(Job, id=job_id)
    
    # Only clients can review freelancers
    if request.user.user_type != 'client':
        messages.error(request, 'Only clients can leave reviews for freelancers.')
        return redirect('jobs:home')
    
    # Check if user is the client for this job
    if job.client != request.user:
        messages.error(request, 'You can only review jobs you posted.')
        return redirect('jobs:home')
    
    # Check if project exists and is completed
    try:
        project = Project.objects.get(job=job)
        if project.status != 'completed':
            messages.error(request, 'You can only review completed projects.')
            return redirect('jobs:project_detail', project_id=project.id)
        reviewed_user = project.freelancer
    except Project.DoesNotExist:
        messages.error(request, 'This job does not have a project yet.')
        return redirect('jobs:job_detail', job_id=job.id)
    
    # Check if review already exists
    if Review.objects.filter(job=job, reviewer=request.user, reviewed_user=reviewed_user).exists():
        messages.warning(request, 'You have already reviewed this freelancer for this job.')
        return redirect('jobs:project_detail', project_id=project.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.job = job
            review.reviewer = request.user
            review.reviewed_user = reviewed_user
            review.save()
            
            # Update freelancer rating if reviewed user is a freelancer
            if reviewed_user.user_type == 'freelancer' and reviewed_user.freelancer_profile:
                profile = reviewed_user.freelancer_profile
                all_reviews = Review.objects.filter(reviewed_user=reviewed_user)
                if all_reviews.exists():
                    avg_rating = sum(r.rating for r in all_reviews) / all_reviews.count()
                    profile.rating = round(avg_rating, 2)
                    profile.save()
            
            # Create notification
            Notification.objects.create(
                user=reviewed_user,
                notification_type='review_received',
                title='New Review',
                message=f"You received a {review.rating}-star review from {request.user.username}",
                related_job=job
            )
            
            messages.success(request, 'Review submitted successfully!')
            return redirect('jobs:project_detail', project_id=project.id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/create_review.html', {
        'form': form,
        'job': job,
        'reviewed_user': reviewed_user,
    })


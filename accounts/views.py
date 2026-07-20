from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, FreelancerProfileForm, ClientProfileForm
from .models import FreelancerProfile, ClientProfile
from jobs.models import Job, Application, Project
from accounts.models import User
from notifications.models import Notification


def register(request):
    if request.user.is_authenticated:
        return redirect('jobs:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('accounts:profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    from django.contrib.auth.views import LoginView
    return LoginView.as_view(template_name='accounts/login.html')(request)


@login_required
def profile(request):
    user = request.user
    context = {}
    
    if user.user_type == 'freelancer':
        profile_obj, created = FreelancerProfile.objects.get_or_create(user=user)
        context['profile'] = profile_obj
        context['profile_form'] = FreelancerProfileForm(instance=profile_obj)
    elif user.user_type == 'client':
        profile_obj, created = ClientProfile.objects.get_or_create(user=user)
        context['profile'] = profile_obj
        context['profile_form'] = ClientProfileForm(instance=profile_obj)
    
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    
    if request.method == 'POST':
        if user.user_type == 'freelancer':
            profile_obj = FreelancerProfile.objects.get(user=user)
            form = FreelancerProfileForm(request.POST, instance=profile_obj)
        else:
            profile_obj = ClientProfile.objects.get(user=user)
            form = ClientProfileForm(request.POST, instance=profile_obj)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        if user.user_type == 'freelancer':
            profile_obj = FreelancerProfile.objects.get(user=user)
            form = FreelancerProfileForm(instance=profile_obj)
        else:
            profile_obj = ClientProfile.objects.get(user=user)
            form = ClientProfileForm(instance=profile_obj)
    
    return render(request, 'accounts/edit_profile.html', {'form': form, 'user_type': user.user_type})


@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    if not request.user.is_superuser and request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('jobs:home')
    
    # Statistics
    total_users = User.objects.count()
    total_clients = User.objects.filter(user_type='client').count()
    total_freelancers = User.objects.filter(user_type='freelancer').count()
    total_jobs = Job.objects.count()
    total_applications = Application.objects.count()
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='active').count()
    completed_projects = Project.objects.filter(status='completed').count()
    
    # Recent activity
    recent_jobs = Job.objects.order_by('-created_at')[:10]
    recent_applications = Application.objects.order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_clients': total_clients,
        'total_freelancers': total_freelancers,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'recent_jobs': recent_jobs,
        'recent_applications': recent_applications,
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)

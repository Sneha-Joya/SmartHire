from django.contrib import admin
from .models import Category, Job, Application, Project, ProjectUpdate, ProjectFeedback


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'status', 'budget', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'client__username')
    date_hierarchy = 'created_at'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'freelancer', 'status', 'proposed_rate', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('job__title', 'freelancer__username', 'proposal')
    date_hierarchy = 'created_at'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('job', 'client', 'freelancer', 'status', 'started_at')
    list_filter = ('status', 'started_at')
    search_fields = ('job__title', 'client__username', 'freelancer__username')
    date_hierarchy = 'started_at'


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ('project', 'freelancer', 'status', 'title', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'project__job__title')
    date_hierarchy = 'created_at'


@admin.register(ProjectFeedback)
class ProjectFeedbackAdmin(admin.ModelAdmin):
    list_display = ('project_update', 'client', 'feedback_type', 'is_approved', 'created_at')
    list_filter = ('feedback_type', 'is_approved', 'created_at')
    search_fields = ('comment', 'client__username')
    date_hierarchy = 'created_at'


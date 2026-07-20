from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.home, name='home'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('post-job/', views.post_job, name='post_job'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('my-projects/', views.my_projects, name='my_projects'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/complete/', views.complete_project, name='complete_project'),
    path('project/<int:project_id>/update/', views.create_project_update, name='create_project_update'),
    path('update/<int:update_id>/feedback/', views.add_project_feedback, name='add_project_feedback'),
    path('job/<int:job_id>/applications/', views.manage_applications, name='manage_applications'),
    path('application/<int:application_id>/accept/', views.accept_application, name='accept_application'),
    path('application/<int:application_id>/reject/', views.reject_application, name='reject_application'),
]


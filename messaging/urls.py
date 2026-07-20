from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversations_list, name='conversations'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('start/<int:user_id>/job/<int:job_id>/', views.start_conversation, name='start_conversation_with_job'),
]



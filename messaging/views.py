from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from accounts.models import User
from jobs.models import Job
from .models import Conversation, Message
from notifications.models import Notification


@login_required
def conversations_list(request):
    """List all conversations for the current user"""
    conversations = Conversation.objects.filter(participants=request.user).distinct()
    # Add other_user for each conversation
    conversations_with_users = []
    for conversation in conversations:
        other_user = conversation.get_other_participant(request.user)
        if other_user:  # Only include conversations with valid other_user
            conversations_with_users.append({
                'conversation': conversation,
                'other_user': other_user,
            })
    return render(request, 'messaging/conversations.html', {'conversations_data': conversations_with_users})


@login_required
def conversation_detail(request, conversation_id):
    """View conversation and send messages"""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    other_user = conversation.get_other_participant(request.user)
    
    if not other_user:
        messages.error(request, 'Invalid conversation.')
        return redirect('messaging:conversations')
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            # Update conversation's updated_at timestamp
            conversation.updated_at = timezone.now()
            conversation.save(update_fields=['updated_at'])
            
            # Mark other messages as read
            if other_user:
                Message.objects.filter(
                    conversation=conversation,
                    sender=other_user,
                    is_read=False
                ).update(is_read=True)
                
                # Create notification for recipient
                Notification.objects.create(
                    user=other_user,
                    notification_type='message_received',
                    title='New Message',
                    message=f"You received a new message from {request.user.username}",
                    related_job=conversation.job if conversation.job else None
                )
            
            return redirect('messaging:conversation_detail', conversation_id=conversation_id)
    
    # Mark messages as read
    if other_user:
        Message.objects.filter(
            conversation=conversation,
            sender=other_user,
            is_read=False
        ).update(is_read=True)
    
    message_list = conversation.messages.all()
    
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'other_user': other_user,
        'messages': message_list,
    })


@login_required
def start_conversation(request, user_id, job_id=None):
    """Start a new conversation with a user"""
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user == request.user:
        messages.error(request, 'You cannot start a conversation with yourself.')
        return redirect('jobs:home')
    
    # Check if conversation already exists
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
        if job_id:
            try:
                job = Job.objects.get(id=job_id)
                conversation.job = job
                conversation.save()
            except Job.DoesNotExist:
                pass
    
    return redirect('messaging:conversation_detail', conversation_id=conversation.id)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.apps import apps
from profiles.models import ClientProfile, FreelancerProfile, User
from django.db.models import Q
from django.utils.timezone import now
from django.conf import settings
from user_messages.models import Message


@login_required
def user_inbox(request):
    """Inbox view for Clients and Freelancers."""
    # Fetch all messages for the logged-in user
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    unread_count = messages.filter(is_read=False).count()

    # Initialize filtered messages
    filtered_messages = messages.none()  # Empty QuerySet to start

    # Role-specific message filtering
    if hasattr(request.user, 'clientprofile'):  # If the user is a client
        try:
            client_messages = messages.filter(sender__freelancerprofile__isnull=False)  # Messages from freelancers
            filtered_messages = client_messages  # Client-specific messages
        except ClientProfile.DoesNotExist:
            pass
    elif hasattr(request.user, 'freelancerprofile'):  # If the user is a freelancer
        try:
            freelancer_messages = messages.filter(sender__clientprofile__isnull=False)  # Messages from clients
            filtered_messages = freelancer_messages  # Freelancer-specific messages
        except FreelancerProfile.DoesNotExist:
            pass

    # Include messages from staff/admins
    staff_messages = messages.filter(sender__is_staff=True)
    filtered_messages = filtered_messages | staff_messages

    # Ensure distinct results to avoid duplicate messages
    filtered_messages = filtered_messages.distinct()

    # Paginate messages
    paginator = Paginator(filtered_messages, 10)  # Show 10 messages per page
    page_number = request.GET.get('page', 1)  # Fetch the requested page number
    try:
        page_messages = paginator.get_page(page_number)
    except (EmptyPage, PageNotAnInteger):  # Handle invalid page numbers gracefully
        page_messages = paginator.page(1)

    # Render inbox template with filtered and paginated messages
    return render(request, 'user_messages/inbox.html', {
        'messages': page_messages,
        'unread_count': unread_count,
    })

@login_required
def sent_messages(request):
    """View for sent messages."""
    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')

    # Paginate messages
    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page')
    page_messages = paginator.get_page(page_number)

    return render(request, 'user_messages/sent.html', {'messages': page_messages})


@login_required
def compose_message(request):
    """Compose new message."""
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        recipient = get_object_or_404(User, username=recipient_username)

        # Role-based validation with user feedback
        if request.user.role == 'FREELANCER' and recipient.role != 'CLIENT':
            messages.error(request, "Freelancers can only send messages to Clients.")
            return redirect('user_messages:compose')
        elif request.user.role == 'CLIENT' and recipient.role != 'FREELANCER':
            messages.error(request, "Clients can only send messages to Freelancers.")
            return redirect('user_messages:compose')

        subject = request.POST.get('subject')
        body = request.POST.get('body')

        Message.objects.create(sender=request.user, recipient=recipient, subject=subject, body=body)
        messages.success(request, "Message sent successfully!")
        return redirect('user_messages:sent')

    return render(request, 'user_messages/compose.html')


@login_required
def message_detail(request, message_id):
    """View detailed message for users and admins."""
    # Fetch the message securely
    message = get_object_or_404(Message, pk=message_id)

    # Check permissions: Regular users can only view if they are sender/recipient; Admins can access all messages
    if request.user not in [message.sender, message.recipient] and not request.user.is_staff:
        messages.error(request, "You are not authorized to view this message.")
        return redirect('user_messages:inbox')

    # Mark message as read for the recipient
    if request.user == message.recipient and not message.is_read:
        message.is_read = True
        message.save()

    # Handle replying via POST
    if request.method == 'POST':
        reply_body = request.POST.get('reply_body', '').strip()
        if reply_body:
            try:
                # Create reply message
                Message.objects.create(
                    sender=request.user,
                    recipient=message.sender if request.user == message.recipient else message.recipient,
                    subject=f"Re: {message.subject}",
                    body=reply_body
                )
                messages.success(request, "Your reply has been sent successfully.")
                # Redirect based on user role (admin or regular user)
                return redirect('user_messages:admin_inbox' if request.user.is_staff else 'user_messages:inbox')
            except Exception as e:
                messages.error(request, f"Failed to send reply: {str(e)}")
                return redirect('user_messages:detail', message_id=message.id)

    # Fetch application attribute if relevant
    application = getattr(message, 'application', None)

    # Render the detail page
    return render(request, 'user_messages/detail.html', {
        'message': message,
        'application': application,
    })

@login_required
def mark_important(request, message_id):
    """Mark a message as important."""
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.is_important = True
    message.save()
    messages.success(request, "Message marked as important.")
    return redirect('user_messages:inbox')


@login_required
def important_messages(request):
    """View important messages."""
    messages = Message.objects.filter(recipient=request.user, is_important=True).order_by('-timestamp')

    # Paginate messages
    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page')
    page_messages = paginator.get_page(page_number)

    return render(request, 'user_messages/important.html', {'messages': page_messages})


@login_required
def delete_message(request, message_id):
    """Delete a message."""
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.delete()
    messages.success(request, "Message deleted successfully.")
    return redirect('user_messages:inbox')


@login_required
def admin_inbox(request):
    """Admin Inbox for viewing messages."""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access the admin inbox.")
        return redirect('user_messages:inbox')

    # Fetch all messages for the admin
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')

    context = {
        'messages': messages,
        'client_messages_count': messages.filter(sender__role="CLIENT").count(),
        'freelancer_messages_count': messages.filter(sender__role="FREELANCER").count(),
        'unread_client_messages_count': messages.filter(sender__role="CLIENT", is_read=False).count(),
        'unread_freelancer_messages_count': messages.filter(sender__role="FREELANCER", is_read=False).count(),
    }
    return render(request, 'user_messages/admin_inbox.html', context)


@login_required
def admin_compose_message(request, message_id=None):
    """Admin compose or reply to messages."""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to compose messages.")
        return redirect('user_messages:inbox')

    # Dynamically fetch the User model
    User = apps.get_model(settings.AUTH_USER_MODEL)

    original_message = None
    if message_id:
        original_message = get_object_or_404(Message, id=message_id)

    if request.method == 'POST':
        recipient_username = request.POST.get('recipient') or original_message.sender.username
        subject = request.POST.get('subject') or f"Re: {original_message.subject}" if original_message else "No Subject"
        body = request.POST.get('body')

        if not body:
            messages.error(request, "Message body cannot be empty.")
            return redirect('user_messages:admin_compose_message', message_id=message_id)

        try:
            recipient = User.objects.get(username=recipient_username)
            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                subject=subject,
                body=body
            )
            messages.success(request, "Message sent successfully.")
            return redirect('user_messages:admin_inbox')
        except User.DoesNotExist:
            messages.error(request, f"Recipient '{recipient_username}' does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'user_messages/compose.html', {
        'original_message': original_message
    })



@login_required
def contact_support(request):
    """View for users to contact admin support."""
    User = apps.get_model(settings.AUTH_USER_MODEL)
    admin_user = User.objects.filter(is_staff=True).first()

    if not admin_user:
        messages.error(request, "No admin user available to contact.")
        return redirect('user_messages:inbox')

    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        # Debug logs for POST data
        print("DEBUG: Subject:", subject)
        print("DEBUG: Body:", body)

        if not subject or not body:
            messages.error(request, "Both subject and message are required.")
            return redirect('user_messages:contact_support')

        try:
            # Debug log for message creation
            print("DEBUG: Admin User:", admin_user)
            new_message = Message.objects.create(
                sender=request.user,
                recipient=admin_user,
                subject=f"{request.user.role}: {subject}",  
                body=body
            )
            print("DEBUG: New Message Created:", new_message)
        except Exception as e:
            # Log any errors during message creation
            print("ERROR: Message creation failed", str(e))
            messages.error(request, "Something went wrong while sending your message.")
            return redirect('user_messages:contact_support')

        messages.success(request, "Your message has been sent to support!")
        return redirect('user_messages:inbox')  

    return render(request, 'user_messages/contact_support.html')

@login_required
def admin_delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.delete()
    messages.success(request, "Message deleted successfully.")
    return redirect('user_messages:admin_inbox')


@login_required
def conversation_history(request, user_id):
    """Conversation history showing relevant messages as threads."""
    other_user = get_object_or_404(User, id=user_id)

    # Fetch all messages exchanged between the logged-in user and the other user
    conversation = Message.objects.filter(
        sender__in=[request.user, other_user],
        recipient__in=[request.user, other_user]
    ).order_by('timestamp')

    return render(request, 'user_messages/conversation_history.html', {
        'conversation': conversation,
        'user': other_user,
    })
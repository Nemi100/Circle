from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from subscription.models import Subscription
from .models import Job, Review, PreviousWork, Message
from profiles.forms import FreelancerProfileForm, ClientProfileForm, EmployerProfileForm, ReviewForm, PreviousWorkForm
from .forms import JobForm, MessageForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User


@login_required
def user_dashboard(request):
    user = request.user
    unread_messages = Message.objects.filter(recipient=user, read=False).count() 

    if hasattr(user, 'employerprofile'):
        profile = user.employerprofile
        user_type = 'employer'
        template = 'dashboard/employer_dashboard.html'
    elif hasattr(user, 'clientprofile'):
        profile = user.clientprofile
        user_type = 'client'
        subscription = Subscription.objects.filter(user=user).first()
        template = 'dashboard/client_dashboard.html'
    elif hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
        user_type = 'freelancer'
        subscription = Subscription.objects.filter(user=user).first()
        template = 'dashboard/freelancer_dashboard.html'
    else:
        profile = None
        user_type = None
        template = 'dashboard/dashboard.html'

    context = {
        'profile': profile,
        'user_type': user_type,
        'subscription': subscription if user_type in ['client', 'freelancer'] else None,
        'profile_exists': profile is not None,
        'unread_messages': unread_messages,
        'include_media': True
    }

    return render(request, template, context)

@login_required
def add_profile(request):
    user = request.user
    if hasattr(user, 'freelancerprofile'):
        form_class = FreelancerProfileForm
        extra_form_class = PreviousWorkForm
    elif hasattr(user, 'clientprofile'):
        form_class = ClientProfileForm
        extra_form_class = None
    else:
        form_class = EmployerProfileForm
        extra_form_class = None

    if request.method == 'POST':
        profile_form = form_class(request.POST, request.FILES)
        if extra_form_class:
            extra_form = extra_form_class(request.POST)
        if profile_form.is_valid() and (not extra_form_class or extra_form.is_valid()):
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            if extra_form_class:
                extra_work = extra_form.save(commit=False)
                extra_work.profile = profile
                extra_work.save()
            return redirect('dashboard:user_dashboard')
    else:
        profile_form = form_class()
        if extra_form_class:
            extra_form = extra_form_class()

    return render(request, 'dashboard/add_profile.html', {
        'profile_form': profile_form,
        'extra_form': extra_form if extra_form_class else None
    })

@login_required
def edit_profile(request):
    user = request.user

    try:
        profile = user.clientprofile
        profile_exists = True
    except ClientProfile.DoesNotExist:
        profile = None
        profile_exists = False

    if request.method == 'POST':
        profile_form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('dashboard:user_dashboard')
    else:
        profile_form = ClientProfileForm(instance=profile)

    return render(request, 'dashboard/edit_profile.html', {
        'profile_form': profile_form,
        'profile': profile,
        'profile_exists': profile_exists
    })

@login_required
def delete_profile(request):
    user = request.user
    if hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
    elif hasattr(user, 'clientprofile'):
        profile = user.clientprofile
    else:
        profile = user.employerprofile
    if request.method == 'POST':
        profile.delete()
        return redirect('dashboard:user_dashboard')
    return render(request, 'dashboard/delete_profile.html', {'profile': profile})

@login_required
def post_job(request):
    if not hasattr(request.user, 'clientprofile'):
        return redirect('dashboard:user_dashboard')  # Only clients should access this view

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user.clientprofile
            job.save()
            return redirect('dashboard:user_dashboard')
    else:
        form = JobForm()
    return render(request, 'dashboard/post_job.html', {'form': form})

@login_required
def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'dashboard/review_list.html', {'reviews': reviews})

@login_required
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'dashboard/review_form.html', {'form': form})

@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'dashboard/review_form.html', {'form': form})

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'dashboard/review_confirm_delete.html', {'review': review})

@login_required
def update_user_type(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserTypeForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard:user_dashboard')
    else:
        form = UserTypeForm(instance=user_profile)
    return render(request, 'dashboard/update_user_type.html', {'form': form})

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    no_new_messages = not messages.exists()
    return render(request, 'dashboard/inbox.html', {'messages': messages,'no_new_messages': no_new_messages})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.recipient != request.user:
        return redirect('dashboard:inbox')
    message.read = True
    message.save()

    if request.method == 'POST':
        reply_form = MessageForm(request.POST, sender=request.user, recipient=message.sender, subject=f"Re: {message.subject}")
        if reply_form.is_valid():
            reply_message = reply_form.save(commit=False)
            reply_message.sender = request.user
            reply_message.recipient = message.sender
            reply_message.save()
            return redirect('dashboard:message_detail', message_id=message.id)
    else:
        reply_form = MessageForm(sender=request.user, recipient=message.sender, subject=f"Re: {message.subject}")

    return render(request, 'dashboard/message_detail.html', {'message': message, 'reply_form': reply_form})


@login_required
def send_message_to_user(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    recipient = job.client.user
    sender = request.user
    subject = f"Regarding your job post: {job.project_title}"

    if request.method == 'POST':
        form = MessageForm(request.POST, sender=sender, recipient=recipient, subject=subject)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.save()
            return redirect('dashboard:user_dashboard')
    else:
        form = MessageForm(sender=sender, recipient=recipient, subject=subject)

    return render(request, 'dashboard/send_message_to_user.html', {'form': form, 'recipient': recipient})

def job_listings(request):
    job_list = Job.objects.all().order_by('project_title')
    paginator = Paginator(job_list, 10)  # Show 10 jobs per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/job_listings.html', {'page_obj': page_obj})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'dashboard/job_detail.html', {'job': job})

@login_required
def delete_job(request):
    user = request.user
    if hasattr(user, 'clientprofile'):
        jobs = Job.objects.filter(client=user.clientprofile)
        if request.method == 'POST':
            job_id = request.POST.get('job_id')
            job = get_object_or_404(Job, id=job_id, client=user.clientprofile)
            job.delete()
            return redirect('dashboard:user_dashboard')
        return render(request, 'dashboard/delete_job.html', {'jobs': jobs})
    return redirect('dashboard:user_dashboard')

@login_required
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home')
    return render(request, 'dashboard/delete_account.html')

@login_required
def delete_job(request):
    user = request.user
    if hasattr(user, 'clientprofile'):
        jobs = Job.objects.filter(client=user.clientprofile)
        if request.method == 'POST':
            job_id = request.POST.get('job_id')
            job = get_object_or_404(Job, id=job_id, client=user.clientprofile)
            job.delete()
            return redirect('dashboard:delete_job')
        return render(request, 'dashboard/delete_job.html', {'jobs': jobs})
    return redirect('dashboard:user_dashboard')




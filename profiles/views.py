from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FreelancerProfileForm, ClientProfileForm
from .models import FreelancerProfile, ClientProfile, SkillCategory
from jobs.models import Job
from user_messages.models import Message
from profiles.models import ClientProfile, AdminActionLog, UserEventLog
from django.contrib.auth.models import User
from profiles.models import User



@login_required
def onboarding(request):
    user = request.user

    # Redirect admins to the admin dashboard
    if user.is_staff:
        return redirect('profiles:admin_dashboard')

    user_type = request.POST.get('user_type')

    # Handle user type selection
    if request.method == 'POST' and user_type:
        if user_type == 'freelancer':
            user.role = 'FREELANCER'
            user.save()

            # Log the user onboarding as Freelancer
            UserEventLog.objects.create(user=user, event='REGISTER')

            messages.success(request, "You are now onboarded as a Freelancer.")
            return redirect('profiles:create_profile')
        elif user_type == 'client':
            user.role = 'CLIENT'
            user.save()

            # Log the user onboarding as Client
            UserEventLog.objects.create(user=user, event='REGISTER')

            messages.success(request, "You are now onboarded as a Client.")
            return redirect('profiles:client_dashboard')

    # Redirect if already onboarded
    if user.role in ['FREELANCER', 'CLIENT']:
        return redirect('profiles:user_dashboard')

    return render(request, 'profiles/onboarding_type.html')



@login_required
def client_dashboard(request):
    context = get_dashboard_context(request.user)

    try:
        client_profile = ClientProfile.objects.get(user=request.user)

        # Count job postings and jobs with applications
        user_jobs = Job.objects.filter(client=client_profile).count()
        jobs_with_applications = Job.objects.filter(client=client_profile, applications__isnull=False).distinct().count()

        context['user_jobs'] = user_jobs
        context['jobs_with_applications'] = jobs_with_applications
    except ClientProfile.DoesNotExist:
        context['user_jobs'] = 0
        context['jobs_with_applications'] = 0
        messages.warning(
            request,
            "You need to create your client profile to access all dashboard features."
        )

    if context['client_profile']:
        completion = context['profile_completion']
        if completion < 100:
            missing = context['client_profile'].missing_fields()
            messages.warning(
                request,
                f"Your profile is {completion}% complete. Missing fields: {', '.join(missing)}."
            )

    return render(request, 'profiles/client_dashboard.html', context)


@login_required
def freelancer_dashboard(request):
    try:
        # Ensure the freelancer profile exists
        profile = request.user.freelancerprofile
        completion = profile.profile_completion_percentage()  # Calculate profile completion
        missing_fields = profile.missing_fields()  # Get list of missing fields

        # Warn about incomplete profiles
        if completion < 100:
            messages.warning(
                request,
                f"Your profile is {completion}% complete. Missing fields: {', '.join(missing_fields)}."
            )
    except FreelancerProfile.DoesNotExist:
        # Redirect to profile creation if no profile exists
        messages.info(request, "You need to create your profile to access the dashboard!")
        return redirect('profiles:create_profile')

    # Add additional context data
    context = get_dashboard_context(request.user)  # Shared data like unread_count
    context.update({
        'profile': profile,
        'profile_completion': completion,
        'missing_fields': missing_fields,
    })

    return render(request, 'profiles/freelancer_dashboard.html', context)


    
def get_dashboard_context(user):
    unread_count = Message.objects.filter(recipient=user, is_read=False).count()  # Count unread messages

    profile_completion = None
    client_profile = None
    if user.role == 'CLIENT':
        try:
            client_profile = ClientProfile.objects.get(user=user)
            profile_completion = client_profile.profile_completion_percentage()
        except ClientProfile.DoesNotExist:
            client_profile = None

    return {
        'unread_count': unread_count,
        'profile_completion': profile_completion,  # For client profile completeness
        'client_profile': client_profile,  # Include ClientProfile
        'user_role': user.role,
    }
    
# Redirect to Role-Specific Dashboards
@login_required
def user_dashboard(request):
    if request.user.is_staff:  # Check if the user is an admin
        return redirect('profiles:admin_dashboard')  # Redirect directly to the admin dashboard
    elif request.user.role == 'FREELANCER':  # Check if the user is a freelancer
        return redirect('profiles:freelancer_dashboard')  # Redirect to freelancer dashboard
    elif request.user.role == 'CLIENT':  # Check if the user is a client
        return redirect('profiles:client_dashboard')  # Redirect to client dashboard
    return redirect('profiles:onboarding')  # Redirect to onboarding if no role is set


# Freelancer Public-Facing Profile
def view_freelancer_profile(request, username):
    profile = get_object_or_404(FreelancerProfile, user__username=username)
    return render(request, 'profiles/view_freelancer_profile.html', {'profile': profile})


@login_required
def freelancer_public_profile(request, username):
    profile = get_object_or_404(FreelancerProfile, user__username=username)
    completion = profile.profile_completion_percentage()

    context = get_dashboard_context(request.user)
    context.update({
        'profile': profile,
        'profile_completion': completion,  
    })

    return render(request, 'profiles/freelancer_public_profile.html', context)


def search_freelancers(request):
    skill = request.GET.get('skill', None)  # Capture skill input
    freelancers = []  # Default empty list for freelancers
    search_performed = False  # Track if a search was performed

    # If there is a skill in the query, perform the search
    if skill:
        search_performed = True
        freelancers = FreelancerProfile.objects.filter(skills__name__icontains=skill)

        # If no results are found
        if not freelancers:
            message = f"No freelancers with '{skill}' skills found. Please try another skill."
        else:
            message = None
    else:
        # Clear results and reset everything for a proper refresh
        skill = None
        freelancers = []  # Ensure no results are displayed
        search_performed = False
        message = None  # No message displayed

    return render(request, 'profiles/search_freelancers.html', {
        'freelancers': freelancers,
        'search_performed': search_performed,
        'message': message,
        'skill': skill  # Pass skill to the template
    })


# Create Profile for Freelancer
@login_required
def create_profile(request):
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    profile, _ = FreelancerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = FreelancerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save user details
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.profile_picture = form.cleaned_data.get('profile_picture')
            profile.user.save()

            # Save profile details
            profile = form.save(commit=False)
            profile.save()
            form.save_m2m()
            messages.success(request, "Profile created successfully!")
            return redirect('profiles:freelancer_dashboard')
    else:
        form = FreelancerProfileForm(instance=profile)

    return render(request, 'profiles/create_profile.html', {'form': form, 'skill_categories': skill_categories})

@login_required
def create_client_profile(request):
    profile, _ = ClientProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Client profile created successfully!")
            return redirect('profiles:client_dashboard')
    else:
        form = ClientProfileForm(instance=profile)

    return render(request, 'profiles/create_client_profile.html', {'form': form})
    

# Edit Profile for Freelancer
@login_required
def edit_profile(request):
    profile, _ = FreelancerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = FreelancerProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profiles:freelancer_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FreelancerProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {
        'form': form,
        'profile': profile,
    })


# Update Client Dashboard
@login_required
def update_client_dashboard(request):
    profile, _ = ClientProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profiles:client_dashboard')

    form = ClientProfileForm(instance=profile)
    return render(request, 'profiles/update_client_profile.html', {'form': form})

@login_required
def update_client_profile(request):
    profile, _ = ClientProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profiles:client_dashboard')
    else:
        form = ClientProfileForm(instance=profile)
    
    return render(request, 'profiles/update_client_profile.html', {'form': form})

# Placeholder Views
def manage_subscription(request):
    return render(request, 'profiles/subscription.html')



@login_required
def delete_account(request):
    user_to_delete = request.user

    if request.method == 'POST':
        # Log the deletion
        UserEventLog.objects.create(user=user_to_delete, event='DELETE')

        # Delete the user account
        user_to_delete.delete()

        messages.success(request, "Your account has been deleted.")
        return redirect('home')

    return render(request, 'profiles/delete_account.html')


@login_required
def client_job_management(request):
    client_jobs = Job.objects.filter(client=request.user.clientprofile)

    return render(request, 'profiles/client_job_management.html', {
        'client_jobs': client_jobs,
    })

def contact_support(request):
    return render(request, 'profiles/contact_support.html')



@login_required
def admin_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_staff:
        return redirect('profiles:user_dashboard')

    # Messaging stats
    from user_messages.models import Message  # Import Message model
    total_messages = Message.objects.filter(recipient=request.user).count()
    unread_messages = Message.objects.filter(recipient=request.user, is_read=False).count()
    important_messages = Message.objects.filter(recipient=request.user, is_important=True).count()

    # Admin stats
    total_users = User.objects.count()  # Total registered users
    total_freelancers = User.objects.filter(role=User.Role.FREELANCER).count()  # Filter freelancers
    total_clients = User.objects.filter(role=User.Role.CLIENT).count()  # Filter clients

    context = {
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'important_messages': important_messages,
        'total_users': total_users,
        'total_freelancers': total_freelancers,
        'total_clients': total_clients,
    }
    return render(request, 'profiles/admin_dashboard.html', context)

@login_required
def admin_user_management(request):
    if not request.user.is_staff:
        return redirect('profiles:user_dashboard')

    if request.user.is_superuser:
        users = User.objects.all()  # Super admins can see all users
    else:
        users = User.objects.filter(role__in=['FREELANCER', 'CLIENT'])  # Regular admins see limited roles

    return render(request, 'profiles/admin_user_management.html', {'users': users})


@login_required
def edit_user(request, user_id):
    # Ensure only admins can edit users
    if not request.user.is_staff:
        return redirect('profiles:user_dashboard')

    # Retrieve the user to be edited
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Update user details based on submitted form
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.role = request.POST.get('role', user.role)
        user.save()
        messages.success(request, "User updated successfully!")
        return redirect('admin_user_management')

    return render(request, 'profiles/edit_user.html', {'user': user})



@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return redirect('profiles:user_dashboard')

    user_to_delete = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Log the deletion
        UserEventLog.objects.create(user=user_to_delete, event='DELETE')

        # Delete the user account
        user_to_delete.delete()

        messages.success(request, "User deleted successfully!")
        return redirect('admin_user_management')

    return render(request, 'profiles/delete_user.html', {'user': user_to_delete})

@login_required
def create_admin(request):
    if not request.user.is_superuser:
        return redirect('profiles:admin_user_management')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        new_admin = User.objects.create_user(username=username, email=email, password=password, role='ADMIN', is_staff=True)
        new_admin.save()
        messages.success(request, "Admin created successfully!")
        return redirect('profiles:admin_user_management')

    return render(request, 'profiles/create_admin.html')


# View for Admin Action Report
@login_required
def admin_report(request):
    if not request.user.is_superuser:
        return redirect('profiles:user_dashboard')

    logs = AdminActionLog.objects.all().order_by('-timestamp')

    # Annotate logs with 'admin_name' for template display
    for log in logs:
        log.admin_name = log.admin.username if log.admin else 'System'

    return render(request, 'profiles/admin_report.html', {'logs': logs})

# View for User Growth Report (Optional)
@login_required
def user_growth_report(request):
    if not request.user.is_superuser:
        return redirect('profiles:user_dashboard')

    registrations = UserEventLog.objects.filter(event='REGISTER').count()
    deletions = UserEventLog.objects.filter(event='DELETE').count()
    net_growth = registrations - deletions

    return render(request, 'profiles/user_growth_report.html', {
        'registrations': registrations,
        'deletions': deletions,
        'net_growth': net_growth,
    })


@login_required
def edit_user(request, user_id):
    if not request.user.is_staff:
        return redirect('profiles:user_dashboard')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        old_username = user.username
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.role = request.POST.get('role', user.role)
        user.save()

        # Log the admin action
        AdminActionLog.objects.create(
            admin=request.user,
            action='EDIT',
            target=f"{old_username} -> {user.username}",
            details=f"Updated email to {user.email}, role to {user.role}"
        )

        messages.success(request, "User updated successfully!")
        return redirect('admin_user_management')

    return render(request, 'profiles/edit_user.html', {'user': user})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import FreelancerProfile, ClientProfile, EmployerProfile, Review, Skill, PreviousWork
from .forms import FreelancerProfileForm, ClientProfileForm, ReviewForm, PreviousWorkForm

def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func

@login_required
def profile_view(request):
    user = request.user
    if hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
        user_type = 'freelancer'
    elif hasattr(user, 'clientprofile'):
        profile = user.clientprofile
        user_type = 'client'
    elif hasattr(user, 'employerprofile'):
        profile = user.employerprofile
        user_type = 'employer'
    else:
        profile = None
        user_type = None  # Handle cases where the profile does not exist

    return render(request, 'profiles/profile.html', {
        'profile': profile,
        'user_type': user_type,
    })

@login_required
def edit_profile(request):
    user = request.user  # Use the currently logged-in user
    if hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
        profile_form = FreelancerProfileForm(request.POST, request.FILES, instance=profile)
        extra_form = PreviousWorkForm(request.POST or None)
        user_type = 'freelancer'
    elif hasattr(user, 'clientprofile'):
        profile = user.clientprofile
        profile_form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        user_type = 'client'
        extra_form = None
    else:
        return redirect('profiles:profile')  # Employers cannot edit their own profiles

    if request.method == 'POST':
        if profile_form.is_valid() and (extra_form is None or extra_form.is_valid()):
            profile_form.save()
            if extra_form:
                extra_work = extra_form.save(commit=False)
                extra_work.profile = profile
                extra_work.save()
            return redirect('profiles:profile')
    else:
        profile_form = FreelancerProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {
        'profile_form': profile_form,
        'extra_form': extra_form,
        'profile': profile,
        'user_type': user_type,
    })

@login_required
def client_profile_view(request):
    user = request.user
    if hasattr(user, 'clientprofile'):
        profile = user.clientprofile
        user_type = 'client'
    else:
        profile = None
        user_type = None  # Handle cases where the profile does not exist

    return render(request, 'profiles/client_profile.html', {
        'profile': profile,
        'user_type': user_type,
    })

@login_required
def client_edit_profile(request):
    user = request.user  # Use the currently logged-in user
    if hasattr(user, 'clientprofile'):
        profile = user.clientprofile
        profile_form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        user_type = 'client'
    else:
        return redirect('profiles:profile')  # Redirect if profile does not exist

    if request.method == 'POST':
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profiles:client_profile_view')
    else:
        profile_form = ClientProfileForm(instance=profile)

    return render(request, 'profiles/client_edit_profile.html', {
        'profile_form': profile_form,
        'profile': profile,
        'user_type': user_type,
    })

@login_required
def leave_review(request, freelancer_username):
    freelancer = get_object_or_404(FreelancerProfile, user__username=freelancer_username)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.freelancer = freelancer
            review.client = request.user.clientprofile
            review.save()
            return redirect('profiles:profile')
    else:
        form = ReviewForm()
    return render(request, 'reviews/leave_review.html', {'form': form, 'freelancer': freelancer})

@superuser_required
def manage_employers(request):
    # Superuser functionality to manage employers
    return render(request, 'profiles/manage_employers.html')

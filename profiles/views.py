from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import FreelancerProfile, EmployerProfile, Review, JobLink, Skill
from .forms import FreelancerProfileForm, EmployerProfileForm, ReviewForm, JobLinkForm

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    if hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
    else:
        profile = get_object_or_404(EmployerProfile, user__username=username)
    return render(request, 'profiles/profile.html', {'profile': profile})

@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.freelancerprofile
    job_link_forms = [JobLinkForm(prefix=str(i)) for i in range(5)]

    if request.method == 'POST':
        profile_form = FreelancerProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            JobLink.objects.filter(profile=profile).delete()
            for job_link_form in job_link_forms:
                if job_link_form.is_valid():
                    job_link = job_link_form.save(commit=False)
                    job_link.profile = profile
                    job_link.save()
            return redirect('profiles:profile', username=username)
    else:
        profile_form = FreelancerProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {
        'profile_form': profile_form,
        'job_link_forms': job_link_forms,
        'profile': profile
    })

@login_required
def leave_review(request, freelancer_username):
    freelancer = get_object_or_404(FreelancerProfile, user__username=freelancer_username)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.freelancer = freelancer
            review.employer = request.user.employerprofile
            review.save()
            return redirect('profiles:profile', username=freelancer.user.username)
    else:
        form = ReviewForm()
    return render(request, 'reviews/leave_review.html', {'form': form, 'freelancer': freelancer})

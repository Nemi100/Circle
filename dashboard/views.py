from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import FreelancerProfile, EmployerProfile, Skill, JobLink
from subscription.models import Subscription
from .models import Job, Review
from .forms import FreelancerProfileForm, EmployerProfileForm, JobForm, ReviewForm, JobLinkForm

@login_required
def user_dashboard(request, username):
    user = get_object_or_404(User, username=username)
    subscription = Subscription.objects.filter(user=user).first()
    
    if hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
        user_type = 'freelancer'
        skills = profile.skills.all()  # Adjusted for multiple skills
    elif hasattr(user, 'employerprofile'):
        profile = user.employerprofile
        user_type = 'employer'
        skills = []

    context = {
        'profile': profile,
        'subscription': subscription,
        'user_type': user_type,
        'skills': skills
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.freelancerprofile if hasattr(user, 'freelancerprofile') else user.employerprofile
    return render(request, 'dashboard/view_profile.html', {'profile': profile})

@login_required
def add_profile(request):
    if request.method == 'POST':
        form = FreelancerProfileForm(request.POST) if 'freelancer' in request.POST else EmployerProfileForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('dashboard:user_dashboard', username=request.user.username)
    else:
        freelancer_form = FreelancerProfileForm()
        employer_form = EmployerProfileForm()
    return render(request, 'dashboard/add_profile.html', {'freelancer_form': freelancer_form, 'employer_form': employer_form})

@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.freelancerprofile if hasattr(user, 'freelancerprofile') else user.employerprofile
    form_class = FreelancerProfileForm if hasattr(user, 'freelancerprofile') else EmployerProfileForm
    job_link_forms = [JobLinkForm(request.POST or None, prefix=str(i)) for i in range(5)]

    if request.method == 'POST':
        profile_form = form_class(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            JobLink.objects.filter(profile=profile).delete()  # Clear existing job links
            for job_link_form in job_link_forms:
                if job_link_form.is_valid():
                    job_link = job_link_form.save(commit=False)
                    job_link.profile = profile
                    job_link.save()
            return redirect('dashboard:user_dashboard', username=username)
    else:
        profile_form = form_class(instance=profile)

    return render(request, 'dashboard/edit_profile.html', {
        'profile_form': profile_form,
        'job_link_forms': job_link_forms,
        'profile': profile
    })

@login_required
def delete_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.freelancerprofile if hasattr(user, 'freelancerprofile') else user.employerprofile
    if request.method == 'POST':
        profile.delete()
        return redirect('dashboard:user_dashboard', username=request.user.username)
    return render(request, 'dashboard/delete_profile.html', {'profile': profile})

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user.employerprofile
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})

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
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'dashboard/review_confirm_delete.html', {'review': review})

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

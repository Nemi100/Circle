from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import FreelancerProfile, EmployerProfile, Skill
from subscription.models import Subscription
from .models import Job, Review
from .forms import FreelancerProfileForm, EmployerProfileForm, JobForm, ReviewForm

@login_required 
def user_dashboard(request, username): 
    user = get_object_or_404(User, username=username) 
    subscription = Subscription.objects.filter(user=user).first() 
    
    if hasattr(user, 'freelancerprofile'): 
        profile = user.freelancerprofile 
        user_type = 'freelancer'
        if profile.skill:
            skills = Skill.objects.filter(category=profile.skill.category)
        else: 
            skills = [] 
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
    if hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
    else:
        profile = user.employerprofile
    return render(request, 'dashboard/view_profile.html', {'profile': profile})

@login_required
def add_profile(request):
    if request.method == 'POST':
        if 'freelancer' in request.POST:
            form = FreelancerProfileForm(request.POST)
            if form.is_valid():
                form.save()
        elif 'employer' in request.POST:
            form = EmployerProfileForm(request.POST)
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
    if hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
        form_class = FreelancerProfileForm
    elif hasattr(user, 'employerprofile'):
        profile = user.employerprofile
        form_class = EmployerProfileForm
    if request.method == 'POST':
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard:user_dashboard', username=request.user.username)
    else:
        form = form_class(instance=profile)
    return render(request, 'dashboard/edit_profile.html', {'form': form, 'profile': profile})

@login_required
def delete_profile(request, username):
    user = get_object_or_404(User, username=username)
    if hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
    elif hasattr(user, 'employerprofile'):
        profile = user.employerprofile
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

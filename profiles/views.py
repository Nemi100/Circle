from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import FreelancerProfile, EmployerProfile, Review
from .forms import ReviewForm
from subscription.models import Subscription

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    if hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
    else:
        profile = get_object_or_404(EmployerProfile, user__username=username)
    return render(request, 'profiles/profile.html', {'profile': profile})

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

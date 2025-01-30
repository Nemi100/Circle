from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from allauth.account.views import SignupView, ConfirmEmailView
from .models import FreelancerProfile, ClientProfile, EmployerProfile, Review, Skill, PreviousWork
from .forms import FreelancerProfileForm, ClientProfileForm, ReviewForm, PreviousWorkForm, UserTypeForm, EmployerProfileForm
from django.urls import reverse
from dashboard.forms import JobForm
from dashboard.models import Job 
from django.contrib import messages



def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func

class CustomSignupView(SignupView):
    template_name = 'account/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.user
        self.request.session['just_registered'] = True
        return redirect('select_user_type')


@login_required
def select_user_type(request):
    user_profile = request.user.userprofile
    if user_profile.user_type:
        return redirect('dashboard:user_dashboard')  # Redirect if user type is already set

    if request.method == 'POST':
        form = UserTypeForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            user_profile.user_type = user_type
            user_profile.save()

            if user_type == 'freelancer':
                # Check if the user already has a FreelancerProfile
                if not FreelancerProfile.objects.filter(user=request.user).exists():
                    FreelancerProfile.objects.create(user=request.user)
                else:
                    messages.error(request, 'You already have a FreelancerProfile.')
            else:
                # Check if the user already has a ClientProfile
                if not ClientProfile.objects.filter(user=request.user).exists():
                    ClientProfile.objects.create(user=request.user)
                else:
                    messages.error(request, 'You already have a ClientProfile.')

            return redirect('dashboard:user_dashboard')
    else:
        form = UserTypeForm()

    return render(request, 'profiles/select_user_type.html', {'form': form})

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
        user_type = None

    context = {
        'profile': profile,
        'user_type': user_type,
        'profile_exists': profile is not None,
        'include_media': True
    }

    if profile:
        if user_type == 'freelancer':
            profile_form = FreelancerProfileForm(instance=profile)
            context['profile_form'] = profile_form
        elif user_type == 'client':
            profile_form = ClientProfileForm(instance=profile)
            context['profile_form'] = profile_form
        elif user_type == 'employer':
            profile_form = EmployerProfileForm(instance=profile)
            context['profile_form'] = profile_form

    return render(request, 'profiles/profile.html', context)


@login_required
def edit_freelancer_profile(request):
    profile = request.user.freelancerprofile
    if request.method == 'POST':
        profile_form = FreelancerProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            # Check if 'first_name' and 'last_name' exist in cleaned_data
            first_name = profile_form.cleaned_data.get('first_name')
            last_name = profile_form.cleaned_data.get('last_name')
            if first_name and last_name:
                profile.user.first_name = first_name
                profile.user.last_name = last_name
                profile.user.save()

            profile_form.save()
            return redirect('profiles:view_profile', username=request.user.username)
    else:
        # Initializes the form with the user's first and last name
        profile_form = FreelancerProfileForm(
            instance=profile, 
            initial={'first_name': profile.user.first_name, 'last_name': profile.user.last_name}
        )

    return render(request, 'profiles/edit_freelancer_profile.html', {
        'profile_form': profile_form,
        'profile': profile,
    })


@login_required
def edit_client_profile(request):
    profile = request.user.clientprofile
    if request.method == 'POST':
        profile_form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profiles:client_profile_view')
    else:
        profile_form = ClientProfileForm(instance=profile)

    return render(request, 'profiles/edit_client_profile.html', {
        'profile_form': profile_form,
        'profile': profile,
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

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

@login_required
def update_user_type(request):
    user_profile = request.user.userprofile
    if user_profile.user_type:
        return redirect('dashboard:user_dashboard')  # Redirect if user type is already set

    if request.method == 'POST':
        form = UserTypeForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard:user_dashboard')
    else:
        form = UserTypeForm(instance=user_profile)
    return render(request, 'profiles/update_user_type.html', {'form': form})

class CustomConfirmEmailView(ConfirmEmailView):
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        return redirect(reverse('profiles:select_user_type'))



@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    
    if hasattr(user, 'freelancerprofile'):
        profile = user.freelancerprofile
    elif hasattr(user, 'clientprofile'):
        profile = user.clientprofile
    elif hasattr(user, 'employerprofile'):
        profile = user.employerprofile
    else:
        profile = None
    
    return render(request, 'dashboard/view_profile.html', {'profile': profile})



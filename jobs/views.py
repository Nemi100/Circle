from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Skill, Application
from .forms import JobForm
from django.core.paginator import Paginator
from user_messages.models import Message 
from profiles.models import FreelancerProfile
from django.db.models import Exists, OuterRef
from django.utils.timezone import now
from django.core.exceptions import ValidationError

def job_list(request):
    # Get the current user's freelancer profile
    freelancer_profile = getattr(request.user, 'freelancerprofile', None)

    # Fetch all skills for the dropdown
    skills = Skill.objects.all()

    # Get the search term from the request
    search_term = request.GET.get('search_term', 'all').strip()

    # Filter jobs based on the search term
    if search_term != 'all' and search_term:
        jobs = Job.objects.filter(skills_required__name__icontains=search_term).order_by('-created_at')
    else:
        jobs = Job.objects.all().order_by('-created_at')

    # Annotate jobs with an "applied" flag for freelancers
    if freelancer_profile:
        jobs = jobs.annotate(
            has_applied=Exists(Application.objects.filter(
                job=OuterRef('pk'),
                freelancer=freelancer_profile
            ))
        )

    # Paginate jobs (9 per page)
    paginator = Paginator(jobs, 9)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'skills': skills,
        'search_term': search_term,
    })

    
@login_required
def create_job(request):
    if not hasattr(request.user, 'clientprofile'):
        messages.error(request, "Access restricted to clients.")
        return redirect('profiles:client_dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)  
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user.clientprofile
            job.save()
            form.save_m2m()  
            messages.success(request, "Job posted successfully!")
            return redirect('profiles:client_dashboard') 
        else:
            messages.error(request, "Form validation failed. Please check your inputs.")
    else:
        form = JobForm()

    return render(request, 'jobs/create_job.html', {'form': form})



@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, client=request.user.clientprofile)

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Job '{job.title}' updated successfully!")
            return redirect('profiles:client_job_management')  
        else:
            messages.error(request, "Form validation failed. Please check your inputs.")
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, client=request.user.clientprofile)

    if request.method == 'POST':
        job.delete()
        messages.success(request, f"Job '{job.title}' deleted successfully!")
        return redirect('profiles:client_dashboard')  

    return render(request, 'jobs/delete_job.html', {'job': job})


def general_jobs_list(request):
    jobs = Job.objects.all()  # Fetch all jobs
    return render(request, 'jobs/general_jobs_list.html', {'jobs': jobs})


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    freelancer_profile = getattr(request.user, 'freelancerprofile', None)

    if not freelancer_profile:
        messages.error(request, "Access restricted to freelancers.")
        return redirect('profiles:freelancer_dashboard')

    # Check if the freelancer has already applied
    if job.applications.filter(freelancer=freelancer_profile).exists():
        messages.error(request, "You have already applied for this job.")
        return redirect('jobs:job_list')

    if request.method == 'POST':
        # Retrieve form data
        linkedin = request.POST.get('linkedin', '').strip()
        portfolio_link = request.POST.get('portfolio_link', '').strip()
        cv = request.FILES.get('cv', None)

        try:
            # Create the application
            application = Application.objects.create(
                job=job,
                freelancer=freelancer_profile,
                linkedin_profile=linkedin,
                portfolio_link=portfolio_link,
                cv=cv
            )

            # Create the message and link the application
            Message.objects.create(
                sender=request.user,
                recipient=job.client.user,
                subject=f"Application for {job.title}",
                body="I’ve applied for your job. Please review my CV and LinkedIn profile.",
                application=application  
            )

            messages.success(request, "Your application has been submitted.")
            return redirect('profiles:freelancer_dashboard')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('jobs:apply_for_job', job_id=job.id)

    return render(request, 'jobs/apply.html', {'job': job})


@login_required
def job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, client=request.user.clientprofile)
    applications = Application.objects.filter(job=job)

    return render(request, 'jobs/job_applications.html', {'job': job, 'applications': applications})

def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_details.html', {'job': job})
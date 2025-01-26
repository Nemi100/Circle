from django.shortcuts import render
from dashboard.models import Job

def index(request):
    jobs = Job.objects.all()  
    return render(request, 'home/index.html', {'jobs': jobs})  

from django.contrib import admin
from .models import FreelancerProfile, EmployerProfile, Skill, Review, Job

admin.site.register(FreelancerProfile)
admin.site.register(EmployerProfile)
admin.site.register(Skill)
admin.site.register(Review)
admin.site.register(Job)

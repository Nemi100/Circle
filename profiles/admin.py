from django.contrib import admin
from .models import FreelancerProfile, ClientProfile, EmployerProfile, Skill, Review, SkillCategory

admin.site.register(FreelancerProfile)
admin.site.register(ClientProfile)
admin.site.register(EmployerProfile)
admin.site.register(Skill)
admin.site.register(SkillCategory)  
admin.site.register(Review)
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('create/', views.create_job, name='create_job'),
    path('list/', views.job_list, name='job_list'),  #freelancers' job list
    path('general/', views.general_jobs_list, name='general_jobs_list'),  # General job list for non-logged-in users
    path('<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('job/<int:job_id>/applications/', views.job_applications, name='job_applications'),
    path('<int:job_id>/details/', views.job_details, name='job_details'),
]

